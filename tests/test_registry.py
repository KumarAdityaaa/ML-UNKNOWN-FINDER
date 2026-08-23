from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.ingestion.registry import CorpusRegistry
from unknown_finder.extraction.novelty import NoveltyResult

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

def test_corpus_registry_persists_novelty_results(tmp_path):
    registry_path = tmp_path / "corpus.json"
    registry = CorpusRegistry(registry_path)

    novelty = NoveltyResult(
        term="adaptive attention",
        novelty_score=0.72,
        reason="rare and specific technical concept",
    )

    papers = [
        PaperRecord(
            paper_id="paper-002",
            title="Novelty Paper",
            source="test",
            novelty_results=[novelty],
        )
    ]

    registry.save(papers)
    loaded = registry.load()

    assert len(loaded) == 1
    assert len(loaded[0].novelty_results) == 1
    assert loaded[0].novelty_results[0].term == "adaptive attention"
    assert loaded[0].novelty_results[0].novelty_score == 0.72
    assert loaded[0].novelty_results[0].reason == (
        "rare and specific technical concept"
    )