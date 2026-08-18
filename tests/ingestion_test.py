from unknown_finder.ingestion.models import PaperRecord


def test_paper_record():
    paper = PaperRecord(
        paper_id="test-001",
        title="Test Paper",
        source="test",
    )

    assert paper.paper_id == "test-001"
    assert paper.title == "Test Paper"
    assert paper.source == "test"