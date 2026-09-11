from unknown_finder.evaluation.models import EvaluationCase, EvaluationDataset
from unknown_finder.evaluation.service import EvaluationService


def test_evaluation_service_compares_baseline_and_candidate():
    dataset = EvaluationDataset(
        cases=[
            EvaluationCase(
                input_text="case one",
                expected="yes",
            ),
            EvaluationCase(
                input_text="case two",
                expected="yes",
            ),
        ]
    )

    service = EvaluationService()

    result = service.compare(
        dataset=dataset,
        baseline_scorer=lambda case: 0.5,
        candidate_scorer=lambda case: 1.0,
    )

    assert result.metric == "candidate_minus_baseline"
    assert result.score == 0.5
