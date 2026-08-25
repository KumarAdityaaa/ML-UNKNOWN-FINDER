from unknown_finder.hypothesis.models import Hypothesis
from unknown_finder.hypothesis.report import format_hypothesis_report


def test_format_hypothesis_report():
    hypotheses = [
        Hypothesis(
            concept_a="attention",
            concept_b="medical imaging",
            evidence_ids=["evidence-001"],
        ),
    ]

    report = format_hypothesis_report(hypotheses)

    assert "Hypotheses" in report
    assert "attention" in report
    assert "medical imaging" in report
    assert "evidence-001" in report

def test_format_hypothesis_report_empty():
    report = format_hypothesis_report([])

    assert report == (
        "Hypotheses\n"
        "==========\n"
        "No hypotheses generated."
    )

def test_format_hypothesis_report_numbers_multiple_hypotheses():
    hypotheses = [
        Hypothesis(
            concept_a="attention",
            concept_b="medical imaging",
            evidence_ids=["evidence-001"],
        ),
        Hypothesis(
            concept_a="transformer",
            concept_b="genomics",
            evidence_ids=[
                "evidence-002",
                "evidence-003",
            ],
        ),
    ]

    report = format_hypothesis_report(hypotheses)

    assert "1. attention <-> medical imaging" in report
    assert "2. transformer <-> genomics" in report
    assert "Evidence: evidence-001" in report
    assert "Evidence: evidence-002, evidence-003" in report

def test_format_hypothesis_report_limit():
    hypotheses = [
        Hypothesis(
            concept_a="attention",
            concept_b="medical imaging",
            evidence_ids=["evidence-001"],
            confidence=0.85,
        ),
        Hypothesis(
            concept_a="transformer",
            concept_b="genomics",
            evidence_ids=["evidence-002"],
        ),
    ]

    report = format_hypothesis_report(
        hypotheses,
        limit=1,
    )

    assert "attention" in report
    assert "medical imaging" in report
    assert "transformer" not in report
    assert "genomics" not in report
    assert "confidence=0.8500" in report