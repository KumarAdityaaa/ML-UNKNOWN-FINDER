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

        papers = []

        for work in response.json()["results"]:
            authors = [
                author["author"]["display_name"]
                for author in work.get("authorships", [])
                if author.get("author")
            ]

            papers.append(
                PaperRecord(
                    paper_id=work["id"],
                    title=work["title"],
                    authors=authors,
                    abstract=None,
                    publication_date=work.get("publication_date"),
                    venue=(
                        work.get("primary_location", {})
                        .get("source", {})
                        .get("display_name")
                    ),
                    doi=work.get("doi"),
                    openalex_id=work["id"],
                    source="openalex",
                    landing_page=work.get("id"),
                    pdf_url=(
                        work.get("primary_location", {})
                        .get("pdf_url")
                    ),
                )
            )

        return papers