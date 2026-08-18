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

def test_deduplicate_by_doi():
    papers = [
        PaperRecord(paper_id="1", title="Paper A", source="openalex", doi="10.1234/ABC"),
        PaperRecord(paper_id="2", title="Paper A", source="pubmed", doi="10.1234/abc"),
    ]

    result = deduplicate(papers)

    assert len(result) == 1


def test_deduplicate_by_arxiv_id():
    papers = [
        PaperRecord(paper_id="1", title="Paper A", source="arxiv", arxiv_id="1234.5678"),
        PaperRecord(paper_id="2", title="Paper A", source="openalex", arxiv_id="1234.5678"),
    ]

    result = deduplicate(papers)

    assert len(result) == 1