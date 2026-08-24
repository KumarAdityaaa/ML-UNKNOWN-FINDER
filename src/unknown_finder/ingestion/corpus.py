from .deduplication import deduplicate
from .models import PaperRecord
from .service import LiteratureService
from .storage import PaperStorage
from unknown_finder.novelty.ranking import RankedUnknown, rank_unknowns
from unknown_finder.novelty.report import format_unknown_report
class LiteratureCorpus:
    def __init__(
        self,
        service: LiteratureService,
        storage: PaperStorage,
    ):
        self.service = service
        self.storage = storage

    def collect(self, query: str, limit: int = 10) -> list[PaperRecord]:
        papers = self.service.search(query, limit)
        papers = deduplicate(papers)
        self.storage.save(papers)
        return papers

    def rank_unknowns(self) -> list[RankedUnknown]:
        papers = self.storage.load()
        return rank_unknowns(papers)

    def unknown_report(self, limit: int | None = None) -> str:
        results = self.rank_unknowns()
        return format_unknown_report(results, limit=limit)