from unknown_finder.ingestion.deduplication import deduplicate
from unknown_finder.ingestion.models import PaperRecord


def test_deduplicate():
    papers = [
        PaperRecord(paper_id="1", title="Paper A", source="test"),
        PaperRecord(paper_id="1", title="Paper A", source="test"),
        PaperRecord(paper_id="2", title="Paper B", source="test"),
    ]

    result = deduplicate(papers)

    assert len(result) == 2
    assert [paper.paper_id for paper in result] == ["1", "2"]