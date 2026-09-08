from unknown_finder.evaluation.metrics import accuracy


def test_accuracy_calculates_correctly():
    assert accuracy(
        true_positives=8,
        true_negatives=9,
        false_positives=1,
        false_negatives=2,
    ) == 0.85


def test_accuracy_returns_zero_when_no_examples():
    assert accuracy(
        true_positives=0,
        true_negatives=0,
        false_positives=0,
        false_negatives=0,
    ) == 0.0
