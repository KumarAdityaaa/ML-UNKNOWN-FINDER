from .base import LiteratureSource
from .models import PaperRecord


class LiteratureService:
    def __init__(self, source: LiteratureSource):
        self.source = source

    def search(self, query: str, limit: int = 10) -> list[PaperRecord]:
        return self.source.search(query, limit)