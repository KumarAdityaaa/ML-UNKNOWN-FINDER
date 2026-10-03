from unknown_finder.evaluation.human import HumanEvaluation
from unknown_finder.evaluation.human_service import average_human_score


def test_average_human_score():
    evaluations = [
        HumanEvaluation("H1", 0.9, 0.8, 0.7),
        HumanEvaluation("H2", 0.6, 0.7, 0.8),
    ]

    assert average_human_score(evaluations) == 0.75


def test_average_human_score_empty():
    assert average_human_score([]) == 0.0
