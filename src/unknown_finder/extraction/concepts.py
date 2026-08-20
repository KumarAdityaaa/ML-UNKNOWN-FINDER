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

    # Document / publication noise
    "figure", "figures", "table", "tables", "paper", "papers",
    "work", "works", "arxiv", "preprint", "copyright",
    "permission", "license", "university", "conference",
    "proceedings", "journal", "author", "authors", "email",
    "abstract", "introduction", "references", "acknowledgements",
}


WORD_PATTERN = re.compile(
    r"\b[A-Za-z][A-Za-z0-9-]{2,}\b"
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


def _extract_terms(text: str) -> list[str]:
    terms: list[str] = []

    matches = list(WORD_PATTERN.finditer(text))

    words = [
        match.group(0).lower()
        for match in matches
    ]

    # Single-word concepts.
    for word in words:
        term = _normalize_term(word)

        if _valid_word(term):
            terms.append(term)

    # Two-word and three-word concepts.
    # Generate n-grams instead of greedily consuming
    # the entire sentence.
    for size in (2, 3):
        for index in range(len(words) - size + 1):
            phrase_words = words[index:index + size]

            if not _valid_phrase(phrase_words):
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