from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.ingestion.storage import PaperStorage
from unknown_finder.extraction.novelty import NoveltyResult

def test_paper_storage(tmp_path):
    path = tmp_path / "papers.json"
    storage = PaperStorage(str(path))

    papers = [
        PaperRecord(
            paper_id="test-001",
            title="Test Paper",
            source="test",
        )
    ]

    storage.save(papers)
    loaded = storage.load()

    assert len(loaded) == 1
    assert loaded[0].paper_id == "test-001"
    assert loaded[0].title == "Test Paper"

def test_paper_storage_persists_novelty_results(tmp_path):
    path = tmp_path / "papers.json"
    storage = PaperStorage(str(path))

    novelty = NoveltyResult(
        term="adaptive attention",
        novelty_score=0.72,
        reason="rare and specific technical concept",
    )

    papers = [
        PaperRecord(
            paper_id="test-002",
            title="Novelty Paper",
            source="test",
            novelty_results=[novelty],
        )
    ]

    storage.save(papers)
    loaded = storage.load()

    assert len(loaded) == 1
    assert len(loaded[0].novelty_results) == 1
    assert loaded[0].novelty_results[0].term == "adaptive attention"
    assert loaded[0].novelty_results[0].novelty_score == 0.72
    assert loaded[0].novelty_results[0].reason == (
        "rare and specific technical concept"
    )