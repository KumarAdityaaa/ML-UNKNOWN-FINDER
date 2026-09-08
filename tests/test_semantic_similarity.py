from unknown_finder.evaluation.semantic_similarity import (
    cosine_similarity,
    semantic_similarity,
)


def test_cosine_similarity_identical_vectors():
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0


def test_cosine_similarity_orthogonal_vectors():
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_semantic_similarity_identical_texts():
    assert semantic_similarity(
        "medical imaging with attention",
        "medical imaging with attention",
    ) == 1.0


def test_semantic_similarity_unrelated_texts_is_lower():
    score = semantic_similarity(
        "medical imaging with attention",
        "quantum computing error correction",
    )

    assert 0.0 <= score < 1.0
