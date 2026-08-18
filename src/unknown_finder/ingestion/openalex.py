import httpx

from .base import LiteratureSource
from .models import PaperRecord


class OpenAlexSource(LiteratureSource):
    BASE_URL = "https://api.openalex.org/works"

    def search(self, query: str, limit: int = 10) -> list[PaperRecord]:
        response = httpx.get(
            self.BASE_URL,
            params={
                "search": query,
                "per-page": limit,
            },
            timeout=30.0,
        )

        response.raise_for_status()

        return [
            PaperRecord(
                paper_id=work["id"],
                title=work["title"],
                source="openalex",
                openalex_id=work["id"],
                doi=work.get("doi"),
            )
            for work in response.json()["results"]
        ]