from unknown_finder.evaluation.models import EvaluationResult
from unknown_finder.evaluation.metrics import evaluate_metric, evaluate_metrics
import pytest

def test_evaluation_result_stores_metric_and_score():
    result = EvaluationResult(metric="gap_precision", score=0.75)

    assert result.metric == "gap_precision"
    assert result.score == 0.75


def test_evaluate_metric_returns_evaluation_result():
    result = evaluate_metric("gap_precision", 0.75)

    assert result.metric == "gap_precision"
    assert result.score == 0.75


def test_evaluate_metric_rejects_score_above_one():
    import pytest

    with pytest.raises(ValueError):
        evaluate_metric("gap_precision", 1.1)


def test_evaluate_metric_rejects_negative_score():
    import pytest

    with pytest.raises(ValueError):
        evaluate_metric("gap_precision", -0.1)


def test_evaluate_metric_rejects_empty_metric_name():
    import pytest

    with pytest.raises(ValueError):
        evaluate_metric("", 0.75)


def test_evaluate_metrics_returns_multiple_results():
    results = evaluate_metrics(
        {
            "gap_precision": 0.80,
            "hypothesis_quality": 0.70,
        }
    )

    assert results[0].metric == "gap_precision"
    assert results[0].score == 0.80
    assert results[1].metric == "hypothesis_quality"
    assert results[1].score == 0.70
def test_evaluate_metrics_returns_empty_list_for_empty_scores():
    from unknown_finder.evaluation.metrics import evaluate_metrics

    assert evaluate_metrics({}) == []
from unknown_finder.evaluation.metrics import precision


def test_precision_calculates_correctly():
    assert precision(true_positives=8, false_positives=2) == 0.8


def test_precision_returns_zero_when_no_predictions():
    assert precision(true_positives=0, false_positives=0) == 0.0
from unknown_finder.evaluation.metrics import recall


def test_recall_calculates_correctly():
    assert recall(true_positives=8, false_negatives=2) == 0.8


def test_recall_returns_zero_when_no_actual_positives():
    assert recall(true_positives=0, false_negatives=0) == 0.0
from unknown_finder.evaluation.metrics import f1_score


def test_f1_score_calculates_correctly():
    assert f1_score(precision=0.8, recall=0.8) == pytest.approx(0.8)


def test_f1_score_returns_zero_when_both_are_zero():
    assert f1_score(precision=0.0, recall=0.0) == 0.0
