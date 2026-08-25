from unknown_finder.gaps.models import Gap
from unknown_finder.gaps.report import format_gap_report


def test_format_gap_report():
    gaps = [
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
            confidence=0.85,
        ),
    ]

    report = format_gap_report(gaps)

    assert "Research Gaps" in report
    assert "attention" in report
    assert "medical imaging" in report
    assert "confidence=0.8500" in report

def test_format_gap_report_empty():
    report = format_gap_report([])

    assert report == (
        "Research Gaps\n"
        "=============\n"
        "No research gaps detected."
    )

def test_format_gap_report_numbers_multiple_gaps():
    gaps = [
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
            confidence=0.85,
        ),
        Gap(
            concept_a="transformer",
            concept_b="genomics",
            confidence=0.70,
        ),
    ]

    report = format_gap_report(gaps)

    assert "1. attention <-> medical imaging" in report
    assert "2. transformer <-> genomics" in report
    assert "confidence=0.8500" in report
    assert "confidence=0.7000" in report

def test_format_gap_report_limit():
    gaps = [
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
            confidence=0.85,
        ),
        Gap(
            concept_a="transformer",
            concept_b="genomics",
            confidence=0.70,
        ),
    ]

    report = format_gap_report(gaps, limit=1)

    assert "attention" in report
    assert "medical imaging" in report
    assert "transformer" not in report
    assert "genomics" not in report