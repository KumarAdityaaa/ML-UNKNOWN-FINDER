from unknown_finder.evaluation.human import HumanEvaluation


def average_human_score(evaluations: list[HumanEvaluation]) -> float:
    if not evaluations:
        return 0.0

    scores = [evaluation.quality_score for evaluation in evaluations]
    return sum(scores) / len(scores)
