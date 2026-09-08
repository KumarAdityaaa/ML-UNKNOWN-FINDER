from unknown_finder.evaluation.models import EvaluationCase


def test_evaluation_case_stores_input_expected_and_actual():
    case = EvaluationCase(
        input_text="attention in medical imaging",
        expected="research gap",
        actual="research gap",
    )

    assert case.input_text == "attention in medical imaging"
    assert case.expected == "research gap"
    assert case.actual == "research gap"


def test_evaluation_case_allows_missing_actual_result():
    case = EvaluationCase(
        input_text="attention in medical imaging",
        expected="research gap",
    )

    assert case.actual is None
