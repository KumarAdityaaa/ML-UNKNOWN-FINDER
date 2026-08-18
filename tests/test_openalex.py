from unknown_finder.ingestion.openalex import OpenAlexSource


def test_openalex_source():
    source = OpenAlexSource()

    assert source is not None


def test_openalex_search():
    source = OpenAlexSource()

    papers = source.search("machine learning", limit=2)

    assert len(papers) <= 2
    assert all(p.source == "openalex" for p in papers)

def test_openalex_metadata():
    source = OpenAlexSource()

    papers = source.search("machine learning", limit=1)
    paper = papers[0]

    assert paper.title
    assert paper.source == "openalex"
    assert paper.openalex_id
    assert paper.paper_id