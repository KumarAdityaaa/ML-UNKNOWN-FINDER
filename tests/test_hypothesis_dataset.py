from unknown_finder.evaluation.hypothesis_similarity import evaluate_hypothesis_dataset
from unknown_finder.evaluation.models import EvaluationCase, EvaluationDataset


def test_evaluate_hypothesis_dataset_returns_average_similarity():
    dataset = EvaluationDataset(
        cases=[
            EvaluationCase(
                input_text="case one",
                expected="Attention improves medical imaging.",
                actual="Attention improves medical imaging.",
            ),
            EvaluationCase(
                input_text="case two",
                expected="Attention improves medical imaging.",
                actual="Quantum computing improves error correction.",
            ),
        ]
    )

    result = evaluate_hypothesis_dataset(dataset)

    assert result.metric == "hypothesis_similarity"
    assert 0.0 <= result.score <= 1.0

def test_evaluate_hypothesis_dataset_empty_returns_zero():
    result = evaluate_hypothesis_dataset(EvaluationDataset())

    assert result.metric == "hypothesis_similarity"
    assert result.score == 0.0
from unknown_finder.evaluation.hypothesis_similarity import evaluate_hypothesis_dataset
from unknown_finder.evaluation.models import EvaluationCase, EvaluationDataset


def test_evaluate_hypothesis_dataset_skips_missing_actual():
    result = evaluate_hypothesis_dataset(
        EvaluationDataset(
            cases=[
                EvaluationCase(
                    input_text="case one",
                    expected="Attention improves imaging.",
                ),
            ]
        )
    )

    assert result.metric == "hypothesis_similarity"
    assert result.score == 0.0
