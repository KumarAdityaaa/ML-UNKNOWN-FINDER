from unknown_finder.evaluation.models import EvaluationCase, EvaluationDataset
from unknown_finder.evaluation.service import EvaluationService


def test_evaluation_service_evaluates_dataset():
    dataset = EvaluationDataset(
        cases=[
            EvaluationCase(
                input_text="case one",
                expected="yes",
                actual="yes",
            ),
            EvaluationCase(
                input_text="case two",
                expected="yes",
                actual="no",
            ),
        ]
    )

    service = EvaluationService()

    result = service.evaluate(
        dataset,
        lambda case: 1.0 if case.expected == case.actual else 0.0,
    )

    assert result.metric == "dataset_score"
    assert result.score == 0.5


def test_evaluation_service_returns_zero_for_empty_dataset():
    service = EvaluationService()

    result = service.evaluate(
        EvaluationDataset(),
        lambda case: 1.0,
    )

    assert result.metric == "dataset_score"
    assert result.score == 0.0
