import pytest

from unknown_finder.evaluation.comparison import compare_scores


def test_compare_scores_returns_difference():
    result = compare_scores(
        baseline=0.70,
        candidate=0.85,
    )

    assert result.metric == "score_difference"
    assert result.score == pytest.approx(0.15)


def test_compare_scores_handles_equal_scores():
    result = compare_scores(
        baseline=0.80,
        candidate=0.80,
    )

    assert result.metric == "score_difference"
    assert result.score == 0.0
