from unknown_finder.gaps.models import Gap


def detect_gaps(
    concept_pairs: list[
        tuple[str, str] | tuple[str, str, float]
    ],
) -> list[Gap]:
    gaps_by_pair: dict[frozenset[str], Gap] = {}

    for item in concept_pairs:
        concept_a = item[0]
        concept_b = item[1]
        confidence = item[2] if len(item) == 3 else 1.0

        if concept_a == concept_b:
            continue

        pair = frozenset((concept_a, concept_b))

        candidate = Gap(
            concept_a=concept_a,
            concept_b=concept_b,
            confidence=confidence,
        )

        existing = gaps_by_pair.get(pair)

        if existing is None or candidate.confidence > existing.confidence:
            gaps_by_pair[pair] = candidate

    return list(gaps_by_pair.values())