from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.ingestion.storage import PaperStorage


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