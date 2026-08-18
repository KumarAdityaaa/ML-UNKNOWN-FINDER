from unknown_finder.ingestion.arxiv import ArxivSource


def test_arxiv_source():
    source = ArxivSource()

    assert source is not None
    assert source.BASE_URL == "https://export.arxiv.org/api/query"