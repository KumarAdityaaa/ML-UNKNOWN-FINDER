import httpx

from .base import LiteratureSource
from .models import PaperRecord


class SemanticScholarSource(LiteratureSource):
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def search(self, query: str, limit: int = 10) -> list[PaperRecord]:
        raise NotImplementedError