from unknown_finder.evidence.models import Claim
from unknown_finder.contradiction.models import Contradiction


def detect_contradictions(
    claims: list[Claim],
) -> list[Contradiction]:
    contradictions: list[Contradiction] = []

    for index, claim_a in enumerate(claims):
        for claim_b in claims[index + 1:]:
            text_a = claim_a.text.lower()
            text_b = claim_b.text.lower()

            if _is_simple_negation_pair(text_a, text_b):
                contradictions.append(
                    Contradiction(
                        claim_a=claim_a.claim_id,
                        claim_b=claim_b.claim_id,
                        paper_a=claim_a.paper_id,
                        paper_b=claim_b.paper_id,
)
                )

    return contradictions


def _is_simple_negation_pair(
    text_a: str,
    text_b: str,
) -> bool:
    negative_a = " does not " in f" {text_a} "
    negative_b = " does not " in f" {text_b} "

    if negative_a == negative_b:
        return False

    positive = text_b if negative_a else text_a
    negative = text_a if negative_a else text_b

    positive = positive.replace(" does not ", " ")
    positive = positive.replace(" doesn't ", " ")
    negative = negative.replace(" does not ", " ")
    negative = negative.replace(" doesn't ", " ")

    positive_words = positive.strip(" .!?").split()
    negative_words = negative.strip(" .!?").split()

    if len(positive_words) != len(negative_words):
        return False

    for positive_word, negative_word in zip(
        positive_words,
        negative_words,
    ):
        if positive_word == negative_word:
            continue

        if (
            positive_word.endswith("s")
            and positive_word[:-1] == negative_word
        ):
            continue

        return False

    return True