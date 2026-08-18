from unknown_finder.ingestion.service import LiteratureService


class FakeSource:
    def search(self, query: str, limit: int = 10):
        return []


def test_literature_service():
    service = LiteratureService(FakeSource())

    result = service.search("machine learning", limit=5)

    assert result == []