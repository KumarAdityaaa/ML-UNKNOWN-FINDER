from unknown_finder.gaps.models import Gap


def detect_gaps(
    concept_pairs: list[tuple[str, str]],
) -> list[Gap]:
    gaps: list[Gap] = []
    seen: set[frozenset[str]] = set()

    for concept_a, concept_b in concept_pairs:
        if concept_a == concept_b:
            continue
        pair = frozenset((concept_a, concept_b))

        if pair in seen:
            continue

        seen.add(pair)

        gaps.append(
            Gap(
                concept_a=concept_a,
                concept_b=concept_b,
            )
        )

    return gaps