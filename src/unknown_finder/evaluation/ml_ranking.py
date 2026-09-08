from unknown_finder.evaluation.semantic_similarity import semantic_similarity


def rank_by_semantic_similarity(
    query: str,
    candidates: list[str],
) -> list[tuple[str, float]]:
    scored = [
        (candidate, semantic_similarity(query, candidate))
        for candidate in candidates
    ]

    return sorted(
        scored,
        key=lambda item: (-item[1], item[0]),
    )
