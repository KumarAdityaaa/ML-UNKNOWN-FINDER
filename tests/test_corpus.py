from unknown_finder.ingestion.corpus import LiteratureCorpus
from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.extraction.novelty import NoveltyResult

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
    def load(self):
        return self.saved

def test_corpus_collect():
    storage = FakeStorage()
    corpus = LiteratureCorpus(FakeService(), storage)

    papers = corpus.collect("machine learning")

    assert len(papers) == 1
    assert papers[0].paper_id == "1"
    assert len(storage.saved) == 1

def test_corpus_rank_unknowns():
    storage = FakeStorage()
    storage.saved = [
        PaperRecord(
            paper_id="1",
            title="Paper A",
            source="test",
            novelty_results=[
                NoveltyResult(
                    term="common method",
                    novelty_score=0.30,
                    reason="common",
                ),
                NoveltyResult(
                    term="adaptive attention",
                    novelty_score=0.90,
                    reason="rare",
                ),
            ],
        ),
        PaperRecord(
            paper_id="2",
            title="Paper B",
            source="test",
            novelty_results=[
                NoveltyResult(
                    term="sparse routing",
                    novelty_score=0.70,
                    reason="rare",
                ),
            ],
        ),
    ]

    corpus = LiteratureCorpus(FakeService(), storage)

    ranked = corpus.rank_unknowns()

    assert [result.term for result in ranked] == [
        "adaptive attention",
        "sparse routing",
        "common method",
    ]