from unknown_finder.evaluation.models import EvaluationDataset, EvaluationResult
from unknown_finder.evaluation.semantic_similarity import semantic_similarity


def hypothesis_similarity(
    expected: str,
    actual: str,
) -> float:
    return semantic_similarity(expected, actual)


def evaluate_hypothesis_pair(
    expected: str,
    actual: str,
) -> EvaluationResult:
    return EvaluationResult(
        metric="hypothesis_similarity",
        score=hypothesis_similarity(expected, actual),
    )


def evaluate_hypothesis_dataset(
    dataset: EvaluationDataset,
) -> EvaluationResult:
    scores = [
        hypothesis_similarity(case.expected, case.actual)
        for case in dataset.cases
        if case.actual is not None
    ]

    if not scores:
        return EvaluationResult(
            metric="hypothesis_similarity",
            score=0.0,
        )

    return EvaluationResult(
        metric="hypothesis_similarity",
        score=sum(scores) / len(scores),
    )
