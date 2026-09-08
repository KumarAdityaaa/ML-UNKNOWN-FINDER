from unknown_finder.evaluation.ml_ranking import rank_by_semantic_similarity


def test_rank_by_semantic_similarity_orders_candidates():
    ranked = rank_by_semantic_similarity(
        "attention mechanisms for medical imaging",
        [
            "quantum error correction",
            "attention in medical image analysis",
            "genomic sequence alignment",
        ],
    )

    assert ranked[0][0] == "attention in medical image analysis"
    assert ranked[0][1] >= ranked[1][1]


def test_rank_by_semantic_similarity_returns_empty_for_no_candidates():
    assert rank_by_semantic_similarity(
        "medical imaging",
        [],
    ) == []
