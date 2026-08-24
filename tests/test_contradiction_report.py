from unknown_finder.contradiction.models import Contradiction
from unknown_finder.contradiction.report import format_contradiction_report


def test_format_contradiction_report():
    contradictions = [
        Contradiction(
            claim_a="claim-001",
            claim_b="claim-002",
            paper_a="paper-001",
            paper_b="paper-002",
        ),
    ]

    report = format_contradiction_report(contradictions)

    assert "Contradictions" in report
    assert "claim-001" in report
    assert "claim-002" in report
    assert "paper-001" in report
    assert "paper-002" in report
    assert "confidence=1.0000" in report

def test_format_contradiction_report_empty():
    report = format_contradiction_report([])

    assert report == (
        "Contradictions\n"
        "==============\n"
        "No contradictions detected."
    )