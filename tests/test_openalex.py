from unknown_finder.ingestion.openalex import OpenAlexSource


def test_openalex_source():
    source = OpenAlexSource()

    assert source is not None


def test_openalex_search():
    source = OpenAlexSource()

    papers = source.search("machine learning", limit=2)

    assert len(papers) <= 2
    assert all(p.source == "openalex" for p in papers)