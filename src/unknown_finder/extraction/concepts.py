import re
from dataclasses import dataclass


@dataclass
class Concept:
    term: str
    frequency: int
    sections: list[str]
    contexts: list[str]
    score: float


STOPWORDS = {
    "about", "after", "again", "against", "also", "among",
    "another", "around", "because", "been", "before", "being",
    "between", "both", "could", "does", "doing", "during",
    "each", "either", "from", "further", "have", "having",
    "here", "into", "itself", "more", "most", "much", "other",
    "ourselves", "over", "same", "should", "some", "such",
    "than", "that", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those",
    "through", "too", "under", "until", "using", "very",
    "was", "were", "what", "when", "where", "which", "while",
    "who", "whom", "with", "would", "your", "yours", "ours",
    "our", "out", "can", "may", "might", "must", "shall",
    "will", "just", "only", "thus", "however", "therefore",
    "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten", "the",

    # Common prose / extraction words.
    "advances",
    "approach",
    "approaches",
    "based",
    "following",
    "information",
    "method",
    "methods",
    "new",
    "result",
    "results",
    "use",
    "used",

    # Document / publication noise.
    "figure",
    "figures",
    "table",
    "tables",
    "paper",
    "papers",
    "work",
    "works",
    "arxiv",
    "preprint",
    "copyright",
    "permission",
    "license",
    "university",
    "conference",
    "proceedings",
    "journal",
    "author",
    "authors",
    "email",
    "abstract",
    "introduction",
    "references",
    "acknowledgements",
}


WORD_PATTERN = re.compile(
    r"\b[A-Za-z][A-Za-z0-9-]{2,}\b"
)


SENTENCE_BOUNDARY_PATTERN = re.compile(
    r"(?<=[.!?])(?:\s+|\n+)"
)


def _valid_word(term: str) -> bool:
    return (
        len(term) >= 4
        and term not in STOPWORDS
        and term.isalpha()
    )


def _valid_phrase(words: list[str]) -> bool:
    if len(words) < 2:
        return False

    if any(word in STOPWORDS for word in words):
        return False

    if any(len(word) < 3 for word in words):
        return False

    # Reject repeated-token phrases such as:
    # "sequence sequence"
    # "model model architecture"
    if len(set(words)) != len(words):
        return False

    return True


def _normalize_term(term: str) -> str:
    if term.endswith("ies") and len(term) > 5:
        return term[:-3] + "y"

    if (
        term.endswith("s")
        and not term.endswith("ss")
        and len(term) > 5
    ):
        return term[:-1]

    return term


def _valid_phrase_shape(words: list[str]) -> bool:
    """
    Reject grammatical and prose fragments that are unlikely
    to represent named technical concepts.

    This is deliberately structural. We do not maintain a
    blacklist of individual phrases such as "never perfect".
    """
    if not words:
        return False

    phrase_stopwords = {
        "advances",
        "approach",
        "approaches",
        "based",
        "following",
        "information",
        "method",
        "methods",
        "new",
        "result",
        "results",
        "use",
        "used",
        "using",
    }

    grammatical_words = {
        "a",
        "an",
        "are",
        "be",
        "been",
        "being",
        "can",
        "could",
        "does",
        "is",
        "may",
        "might",
        "must",
        "our",
        "should",
        "their",
        "this",
        "those",
        "these",
        "was",
        "were",
        "will",
        "would",
        "we",
        "you",
    }

    # Adverbs / discourse markers that commonly start prose
    # fragments rather than technical concepts.
    discourse_words = {
        "always",
        "already",
        "also",
        "even",
        "ever",
        "finally",
        "further",
        "generally",
        "however",
        "instead",
        "just",
        "more",
        "never",
        "often",
        "only",
        "rather",
        "really",
        "simply",
        "still",
        "thus",
        "therefore",
        "usually",
    }

    # Reject prose/action words at the beginning.
    if words[0] in phrase_stopwords:
        return False

    if words[0] in grammatical_words:
        return False

    if words[0] in discourse_words:
        return False

    # A technical phrase should not contain a grammatical
    # auxiliary/pronoun in the middle.
    if any(word in grammatical_words for word in words):
        return False

    # Discourse markers inside short n-grams are also strong
    # evidence that the phrase came from surrounding prose.
    if any(word in discourse_words for word in words):
        return False

    # "but", "and", "or", etc. usually indicate that the
    # extractor captured surrounding prose rather than a
    # standalone concept.
    conjunctions = {
        "and",
        "but",
        "or",
        "nor",
    }

    if any(word in conjunctions for word in words):
        return False

    # Possessive/prose fragments such as:
    # "its application"
    # "their method"
    # "our model"
    possessives = {
        "her",
        "his",
        "its",
        "our",
        "their",
        "your",
    }

    if any(word in possessives for word in words):
        return False

    return True


def _sentence_words(text: str) -> list[list[str]]:
    """
    Extract words sentence-by-sentence.

    Keeping sentence boundaries prevents n-grams from being
    created across punctuation boundaries.
    """
    normalized_text = re.sub(r"\s+", " ", text).strip()

    if not normalized_text:
        return []

    sentences = SENTENCE_BOUNDARY_PATTERN.split(
        normalized_text
    )

    result: list[list[str]] = []

    for sentence in sentences:
        matches = WORD_PATTERN.finditer(sentence)

        words = [
            match.group(0).lower()
            for match in matches
        ]

        if words:
            result.append(words)

    return result


def _extract_terms(text: str) -> list[str]:
    terms: list[str] = []

    sentences = _sentence_words(text)

    # Single-word concepts.
    for words in sentences:
        for word in words:
            term = _normalize_term(word)

            if _valid_word(term):
                terms.append(term)

    # Multi-word concepts are generated only within the same
    # sentence.
    for words in sentences:
        for size in (2, 3):
            for index in range(len(words) - size + 1):
                phrase_words = words[index:index + size]

                if not _valid_phrase(phrase_words):
                    continue

                if not _valid_phrase_shape(phrase_words):
                    continue

                phrase = " ".join(phrase_words)

                if len(phrase) >= 8:
                    terms.append(phrase)

    return terms


def extract_concepts(
    sections,
    *,
    min_frequency: int = 2,
) -> list[Concept]:
    concept_data: dict[str, dict] = {}

    for section in sections:
        terms = _extract_terms(section.text)

        for term in terms:
            if term not in concept_data:
                concept_data[term] = {
                    "frequency": 0,
                    "sections": set(),
                    "contexts": [],
                }

            data = concept_data[term]

            data["frequency"] += 1
            data["sections"].add(section.heading)

            if len(data["contexts"]) < 3:
                index = section.text.lower().find(term)

                if index >= 0:
                    start = max(0, index - 80)
                    end = min(
                        len(section.text),
                        index + len(term) + 120,
                    )

                    context = section.text[start:end].strip()

                    if context:
                        data["contexts"].append(context)

    concepts: list[Concept] = []

    for term, data in concept_data.items():
        if data["frequency"] < min_frequency:
            continue

        score = (
            data["frequency"]
            * (1 + 0.25 * len(data["sections"]))
            * (1.5 if " " in term else 1.0)
        )

        concepts.append(
            Concept(
                term=term,
                frequency=data["frequency"],
                sections=sorted(data["sections"]),
                contexts=data["contexts"],
                score=round(score, 4),
            )
        )

    concepts.sort(
        key=lambda concept: (
            -concept.score,
            -concept.frequency,
            concept.term,
        )
    )

    return concepts