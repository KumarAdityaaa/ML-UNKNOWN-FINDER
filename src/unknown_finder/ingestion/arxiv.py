import httpx

from .base import LiteratureSource
from .models import PaperRecord


class ArxivSource(LiteratureSource):
    BASE_URL = "https://export.arxiv.org/api/query"

    def search(self, query: str, limit: int = 10) -> list[PaperRecord]:
        response = httpx.get(
            self.BASE_URL,
            params={
                "search_query": f"all:{query}",
                "max_results": limit,
            },
            timeout=30.0,
        )
        response.raise_for_status()

        return []