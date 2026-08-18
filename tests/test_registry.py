from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.ingestion.registry import CorpusRegistry


def test_corpus_registry(tmp_path):
    registry_path = tmp_path / "corpus.json"

    papers = [
        PaperRecord(
            paper_id="paper-001",
            title="Test Paper",
            source="test",
        )
    ]

    registry = CorpusRegistry(registry_path)

    registry.save(papers)

    loaded = registry.load()

    assert len(loaded) == 1
    assert loaded[0].paper_id == "paper-001"
    assert loaded[0].title == "Test Paper"
    assert loaded[0].source == "test"