import pytest

from unknown_finder.evaluation.human import HumanEvaluation


def test_human_evaluation_accepts_valid_scores():
    evaluation = HumanEvaluation(
        hypothesis="Test hypothesis",
        relevance=0.8,
        testability=0.9,
        novelty=0.7,
    )

    assert evaluation.relevance == 0.8


def test_human_evaluation_rejects_invalid_scores():
    with pytest.raises(ValueError):
        HumanEvaluation(
            hypothesis="Test hypothesis",
            relevance=1.1,
            testability=0.9,
            novelty=0.7,
        )
