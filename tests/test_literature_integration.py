from unknown_finder.ingestion.arxiv import ArxivSource
from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.ingestion.openalex import OpenAlexSource
from unknown_finder.ingestion.pubmed import PubMedSource
from unknown_finder.ingestion.semantic_scholar import SemanticScholarSource


def test_all_sources_are_literature_sources():
    sources = [
        OpenAlexSource(),
        ArxivSource(),
        PubMedSource(),
        SemanticScholarSource(),
    ]

    assert all(hasattr(source, "search") for source in sources)


def test_paper_record_normalization():
    paper = PaperRecord(
        paper_id="test-001",
        title="Integration Test",
        source="test",
    )

    assert paper.model_dump()["source"] == "test"