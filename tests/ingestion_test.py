from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.extraction.novelty import NoveltyResult

def test_paper_record():
    paper = PaperRecord(
        paper_id="test-001",
        title="Test Paper",
        source="test",
    )

    assert paper.paper_id == "test-001"
    assert paper.title == "Test Paper"
    assert paper.source == "test"

    from unknown_finder.extraction.novelty import NoveltyResult


def test_paper_record_stores_novelty_results():
    novelty = NoveltyResult(
        term="adaptive attention",
        novelty_score=0.72,
        reason="rare and specific technical concept",
    )

    paper = PaperRecord(
        paper_id="1234",
        title="Test Paper",
        source="test",
        novelty_results=[novelty],
    )

    assert len(paper.novelty_results) == 1
    assert paper.novelty_results[0].term == "adaptive attention"
    assert paper.novelty_results[0].novelty_score == 0.72
    assert paper.novelty_results[0].reason == (
        "rare and specific technical concept"
    )