from unknown_finder.evaluation.models import EvaluationResult


def evaluate_metric(
    metric: str,
    score: float,
) -> EvaluationResult:
    if not metric.strip():
        raise ValueError("metric name must not be empty")

    if not 0.0 <= score <= 1.0:
        raise ValueError("score must be between 0.0 and 1.0")

    return EvaluationResult(
        metric=metric,
        score=score,
    )


def evaluate_metrics(
    scores: dict[str, float],
) -> list[EvaluationResult]:
    return [
        evaluate_metric(metric, score)
        for metric, score in scores.items()
    ]


def precision(
    true_positives: int,
    false_positives: int,
) -> float:
    total = true_positives + false_positives

    if total == 0:
        return 0.0

    return true_positives / total


def recall(
    true_positives: int,
    false_negatives: int,
) -> float:
    total = true_positives + false_negatives

    if total == 0:
        return 0.0

    return true_positives / total


def f1_score(
    precision: float,
    recall: float,
) -> float:
    total = precision + recall

    if total == 0:
        return 0.0

    return 2 * precision * recall / total

def accuracy(
    true_positives: int,
    true_negatives: int,
    false_positives: int,
    false_negatives: int,
) -> float:
    total = (
        true_positives
        + true_negatives
        + false_positives
        + false_negatives
    )

    if total == 0:
        return 0.0

    return (true_positives + true_negatives) / total
