from unknown_finder.evaluation.models import EvaluationResult


def compare_scores(
    baseline: float,
    candidate: float,
) -> EvaluationResult:
    return EvaluationResult(
        metric="score_difference",
        score=candidate - baseline,
    )
