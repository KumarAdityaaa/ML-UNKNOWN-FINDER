from unknown_finder.ingestion.base import LiteratureSource


def test_literature_source_is_abstract():
    assert LiteratureSource.__abstractmethods__ == {"search"}