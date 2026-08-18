from unknown_finder.ingestion.openalex import OpenAlexSource


def test_openalex_source():
    source = OpenAlexSource()

    assert source is not None