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

    def test_paper_record_stores_analysis_results():
        paper = PaperRecord(
            paper_id="123",
            title="Test Paper",
            source="test",
            concepts=[
                {
                    "term": "attention mechanism",
                    "frequency": 3,
                    "sections": ["Methods"],
                    "contexts": ["attention mechanism improves alignment"],
                    "score": 4.5,
                }
            ],
            novelty_results=[
                {
                    "term": "attention mechanism",
                    "novelty_score": 0.72,
                    "reason": "rare and specific technical concept",
                }
            ],
        )

        assert paper.concepts[0]["term"] == "attention mechanism"
        assert paper.novelty_results[0]["novelty_score"] == 0.72