import httpx

from .base import LiteratureSource
from .models import PaperRecord


class ArxivSource(LiteratureSource):
    BASE_URL = "https://export.arxiv.org/api/query"

    def search(self, query: str, limit: int = 10) -> list[PaperRecord]:
        raise NotImplementedError