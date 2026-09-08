from unknown_finder.evaluation.models import EvaluationCase, EvaluationDataset


def test_evaluation_dataset_stores_cases():
    dataset = EvaluationDataset(
        cases=[
            EvaluationCase(
                input_text="attention in medical imaging",
                expected="research gap",
            ),
        ]
    )

    assert len(dataset.cases) == 1
    assert dataset.cases[0].expected == "research gap"


def test_evaluation_dataset_size():
    dataset = EvaluationDataset(
        cases=[
            EvaluationCase(
                input_text="attention in medical imaging",
                expected="research gap",
            ),
            EvaluationCase(
                input_text="transformer in genomics",
                expected="hypothesis",
            ),
        ]
    )

    assert dataset.size == 2
