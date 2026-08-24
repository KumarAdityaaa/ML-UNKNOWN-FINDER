from unknown_finder.novelty.ranking import RankedUnknown
from unknown_finder.novelty.report import format_unknown_report


def test_format_unknown_report():
    results = [
        RankedUnknown(
            term="adaptive attention",
            novelty_score=0.90,
            reason="rare and specific technical concept",
            paper_id="paper-002",
            paper_title="Paper Two",
            source_paper_ids=["paper-001", "paper-002"],
        ),
    ]

    report = format_unknown_report(results)

    assert "Unknown Concepts" in report
    assert "adaptive attention" in report
    assert "score=0.9000" in report
    assert "Paper Two" in report
    assert "paper-002" in report
    assert "Sources: 2 paper(s)" in report


def test_format_unknown_report_empty():
    assert format_unknown_report([]) == "No unknowns found."


def test_format_unknown_report_limit():
    results = [
        RankedUnknown(
            term="first concept",
            novelty_score=0.90,
            reason="rare",
            paper_id="paper-001",
            paper_title="First Paper",
            source_paper_ids=["paper-001"],
        ),
        RankedUnknown(
            term="second concept",
            novelty_score=0.80,
            reason="rare",
            paper_id="paper-002",
            paper_title="Second Paper",
            source_paper_ids=["paper-002"],
        ),
    ]

    report = format_unknown_report(results, limit=1)

    assert "first concept" in report
    assert "second concept" not in report