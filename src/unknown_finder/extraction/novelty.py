from dataclasses import dataclass

from .concepts import Concept


@dataclass
class NoveltyResult:
    term: str
    novelty_score: float
    reason: str


PDF_FRAGMENT_WORDS = {
    "abs",
    "corr",
    "doi",
    "vol",
    "volume",
    "issue",
    "isbn",
    "issn",
}


GRAMMATICAL_FRAGMENT_WORDS = {
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
    "should",
    "was",
    "were",
    "will",
    "would",
}


POSSESSIVE_FRAGMENT_WORDS = {
    "her",
    "his",
    "its",
    "our",
    "their",
    "your",
}


FRAGMENT_HEAD_WORDS = {
    "missing",
    "showing",
    "show",
    "using",
    "used",
    "given",
    "following",
    "including",
    "indicating",
    "indicates",
    "suggesting",
    "suggests",
    "providing",
    "provides",
    "allowing",
    "allows",
}


GENERIC_TERMS = {
    "approach",
    "approaches",
    "come",
    "method",
    "methods",
    "observe",
    "paper",
    "result",
    "results",
    "study",
    "work",
}


NAME_LIKE_TERMS = {
    "alex",
    "anna",
    "ba",
    "bengio",
    "britz",
    "denny",
    "geoffrey",
    "geoffrey e hinton",
    "ilya",
    "jimmy",
    "jamie",
    "jason",
    "kyunghyun",
    "luong",
    "minh",
    "oriol",
    "oriol vinyals",
    "quoc",
    "sutskever",
    "vinyals",
}


METADATA_ARTIFACT_WORDS = {
    "acl",
    "arxiv",
    "com",
    "conference",
    "copyright",
    "email",
    "page",
    "pages",
    "proceeding",
    "proceedings",
    "university",
}


PHRASE_ARTIFACT_WORDS = {
    "and",
    "or",
    "but",
    "for",
    "from",
    "into",
    "of",
    "on",
    "to",
    "with",
}


NON_TECHNICAL_PHRASES = {
    "are missing",
    "are shown",
    "can be",
    "come from",
    "could be",
    "does not",
    "does not use",
    "for example",
    "is used",
    "may be",
    "must be",
    "not use",
    "our model",
    "the model",
    "the paper",
    "this model",
    "this paper",
    "we use",
}


def _looks_like_name(term: str) -> bool:
    if term in NAME_LIKE_TERMS:
        return True

    words = term.split()

    return any(word in NAME_LIKE_TERMS for word in words)


def _is_generic(term: str) -> bool:
    return term in GENERIC_TERMS


def _is_phrase_artifact(term: str) -> bool:
    words = term.split()

    if len(words) < 2:
        return False

    return (
        words[0] in PHRASE_ARTIFACT_WORDS
        or words[-1] in PHRASE_ARTIFACT_WORDS
    )


def _is_non_technical_phrase(term: str) -> bool:
    return term in NON_TECHNICAL_PHRASES


def _is_extraction_fragment(term: str) -> bool:
    """
    Detect short phrases that are likely PDF extraction or
    sentence fragments rather than technical concepts.

    This targets structural properties of extracted language
    instead of maintaining a large list of individual bad
    phrases.
    """
    words = term.lower().split()

    if not words:
        return True

    if any(word in PDF_FRAGMENT_WORDS for word in words):
        return True

    if len(words) >= 2 and words[0] in GRAMMATICAL_FRAGMENT_WORDS:
        return True

    if len(words) >= 2 and words[0] in POSSESSIVE_FRAGMENT_WORDS:
        return True

    if len(words) >= 2 and words[0] in FRAGMENT_HEAD_WORDS:
        return True

    return False


def _is_metadata_artifact(concept: Concept) -> bool:
    """
    Detect concepts that are likely PDF metadata, page-header,
    venue, URL, citation, or sentence-extraction artifacts.

    Person names are normally retained so they can be scored
    and explained. Reference-section author phrases are treated
    separately: known author/name phrases are removed, while
    technical phrases such as "adaptive attention" remain
    eligible.
    """
    term = concept.term.lower().strip()
    words = term.split()

    if not words:
        return True

    if _is_extraction_fragment(term):
        return True

    if any(word in METADATA_ARTIFACT_WORDS for word in words):
        return True

    reference_only = (
        len(concept.sections) == 1
        and concept.sections[0].strip().lower()
        in {"references", "acknowledgements"}
    )

    if (
        reference_only
        and len(words) >= 2
        and _looks_like_name(term)
    ):
        return True

    if (
        reference_only
        and len(words) == 1
        and not _looks_like_name(term)
    ):
        return True

    return False


def _technical_signal(term: str) -> float:
    """
    Estimate whether a term looks like a technical concept.

    This is intentionally deterministic and lightweight.
    It does not claim semantic understanding.

    Multi-word phrases receive a specificity advantage,
    but single words can still be technically meaningful.
    """
    words = term.split()

    if len(words) >= 3:
        return 1.0

    if len(words) == 2:
        return 0.95

    if len(term) >= 10:
        return 1.0

    if len(term) >= 8:
        return 0.9

    if term.endswith(
        (
            "tion",
            "sion",
            "ment",
            "ness",
            "ity",
            "ing",
            "ization",
            "isation",
        )
    ):
        return 0.85

    if len(term) >= 6:
        return 0.75

    return 0.5


def _phrase_specificity(term: str) -> float:
    """
    Estimate how much additional information a phrase provides
    compared with an isolated word.

    This is deliberately structural rather than semantic.
    """
    words = term.split()

    if len(words) >= 3:
        return 1.0

    if len(words) == 2:
        return 0.85

    return 0.35

def _apply_phrase_dominance(
    results: list[NoveltyResult],
) -> list[NoveltyResult]:
    """
    Reduce isolated-word candidates when a strong multi-word
    concept containing that word is also present.

    This prevents a generic component such as "additive" from
    competing directly with the more informative concept
    "additive attention".
    """
    strong_phrases = [
        result
        for result in results
        if len(result.term.split()) >= 2
        and result.novelty_score >= 0.55
    ]

    adjusted: list[NoveltyResult] = []

    for result in results:
        words = result.term.split()

        if len(words) == 1:
            containing_phrases = [
                phrase
                for phrase in strong_phrases
                if result.term in phrase.term.split()
            ]

            if containing_phrases:
                strongest = max(
                    phrase.novelty_score
                    for phrase in containing_phrases
                )

                if strongest > result.novelty_score:
                    result = NoveltyResult(
                        term=result.term,
                        novelty_score=round(
                            result.novelty_score * 0.75,
                            4,
                        ),
                        reason=(
                            "isolated component of a stronger "
                            "technical phrase"
                        ),
                    )

        adjusted.append(result)

    return adjusted

def _score_concept(concept: Concept) -> tuple[float, str]:
    frequency = max(concept.frequency, 1)
    section_count = max(len(concept.sections), 1)

    frequency_signal = 1.0 / frequency
    coverage_signal = 1.0 / section_count
    score_signal = 1.0 / (1.0 + concept.score)

    technical_signal = _technical_signal(concept.term)
    specificity_signal = _phrase_specificity(concept.term)

    novelty = (
        0.30 * frequency_signal
        + 0.20 * coverage_signal
        + 0.10 * score_signal
        + 0.25 * technical_signal
        + 0.15 * specificity_signal
    )

    if _is_phrase_artifact(concept.term):
        novelty *= 0.10
        reason = "phrase boundary artifact"

    elif _is_generic(concept.term):
        novelty *= 0.25
        reason = "generic term with weak novelty signal"

    elif _looks_like_name(concept.term):
        novelty *= 0.10
        reason = "likely person-name or author artifact"

    elif _is_non_technical_phrase(concept.term):
        novelty *= 0.10
        reason = "non-technical language fragment"

    elif specificity_signal >= 0.85 and frequency <= 3:
        reason = "rare and specific technical concept"

    elif frequency <= 3 and section_count <= 2:
        reason = "rare and localized technical concept"

    elif frequency <= 5 and section_count <= 3:
        reason = (
            "infrequent technical concept "
            "with limited section coverage"
        )

    elif specificity_signal >= 0.85 and section_count <= 2:
        reason = "specific technical concept concentrated in few sections"

    elif section_count <= 2:
        reason = "technical concept concentrated in few sections"

    else:
        reason = "relatively common technical concept"

    novelty = max(0.0, min(1.0, novelty))

    return round(novelty, 4), reason


def score_novelty(
    concepts: list[Concept],
) -> list[NoveltyResult]:
    results: list[NoveltyResult] = []

    for concept in concepts:
        if _is_metadata_artifact(concept):
            continue

        score, reason = _score_concept(concept)

        results.append(
            NoveltyResult(
                term=concept.term,
                novelty_score=score,
                reason=reason,
            )
        )
    results = _apply_phrase_dominance(results)

    results.sort(
        key=lambda result: (
            -result.novelty_score,
            result.term,
        )
    )

    return results

