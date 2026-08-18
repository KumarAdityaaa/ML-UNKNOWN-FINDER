from unknown_finder.ingestion.corpus import LiteratureCorpus
from unknown_finder.ingestion.models import PaperRecord


class FakeService:
    def search(self, query: str, limit: int = 10):
        return [
            PaperRecord(
                paper_id="1",
                title="Paper A",
                source="test",
            ),
            PaperRecord(
                paper_id="1",
                title="Paper A",
                source="test",
            ),
        ]


class FakeStorage:
    def __init__(self):
        self.saved = []

    def save(self, papers):
        self.saved = papers


def test_corpus_collect():
    storage = FakeStorage()
    corpus = LiteratureCorpus(FakeService(), storage)

    papers = corpus.collect("machine learning")

    assert len(papers) == 1
    assert papers[0].paper_id == "1"
    assert len(storage.saved) == 1