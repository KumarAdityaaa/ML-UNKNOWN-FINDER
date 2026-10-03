import pytest

from unknown_finder.evaluation.ablation import AblationResult


def test_ablation_score_difference():
    result = AblationResult(
        baseline_score=0.8,
        ablated_score=0.6,
    )

    assert result.score_difference == pytest.approx(-0.2)


def test_ablation_equal_scores():
    result = AblationResult(
        baseline_score=0.7,
        ablated_score=0.7,
    )

    assert result.score_difference == 0.0


def test_ablation_rejects_invalid_score():
    with pytest.raises(ValueError):
        AblationResult(
            baseline_score=1.1,
            ablated_score=0.6,
        )
from unknown_finder.evaluation.ablation import AblationResult, evaluate_ablation


def test_evaluate_ablation():
    result = evaluate_ablation(
        baseline_score=0.8,
        ablated_score=0.6,
    )

    assert isinstance(result, AblationResult)
    assert result.score_difference == pytest.approx(-0.2)
