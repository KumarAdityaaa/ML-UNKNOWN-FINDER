import pytest

from unknown_finder.evaluation.models import HypothesisEvaluation


def test_hypothesis_evaluation_quality_score():
    evaluation = HypothesisEvaluation(
        hypothesis="Attention improves medical imaging.",
        relevance=1.0,
        testability=0.8,
        novelty=0.6,
    )

    assert evaluation.quality_score == pytest.approx(0.8)
