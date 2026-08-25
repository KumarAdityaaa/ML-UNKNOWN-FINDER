from unknown_finder.gaps.models import Gap
from unknown_finder.hypothesis.models import Hypothesis


def generate_hypotheses(
    concept_pairs: list[
        tuple[str, str]
        | tuple[str, str, list[str]]
        | Gap
    ],
) -> list[Hypothesis]:
    hypotheses: list[Hypothesis] = []

    for item in concept_pairs:
        if isinstance(item, Gap):
            concept_a = item.concept_a
            concept_b = item.concept_b
        else:
            concept_a = item[0]
            concept_b = item[1]

        evidence_ids = item[2] if not isinstance(item, Gap) and len(item) == 3 else []

        hypotheses.append(
            Hypothesis(
                concept_a=concept_a,
                concept_b=concept_b,
                evidence_ids=evidence_ids,
            )
        )

    return hypotheses