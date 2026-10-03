import pytest

from unknown_finder.evaluation.hypothesis_similarity import hypothesis_similarity


def test_hypothesis_similarity_returns_one_for_identical_hypotheses():
    assert hypothesis_similarity(
        "Attention improves medical image analysis.",
        "Attention improves medical image analysis.",
    ) == pytest.approx(1.0)


def test_hypothesis_similarity_returns_lower_score_for_different_hypotheses():
    score = hypothesis_similarity(
        "Attention improves medical image analysis.",
        "Quantum computing improves error correction.",
    )

    assert 0.0 <= score < 1.0

from unknown_finder.evaluation.hypothesis_similarity import evaluate_hypothesis_pair


def test_evaluate_hypothesis_pair_returns_evaluation_result():
    result = evaluate_hypothesis_pair(
        "Attention improves medical image analysis.",
        "Attention improves medical image analysis.",
    )

    assert result.metric == "hypothesis_similarity"
    assert result.score == pytest.approx(1.0)
