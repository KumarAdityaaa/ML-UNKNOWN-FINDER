import httpx

from .base import LiteratureSource
from .models import PaperRecord


class PubMedSource(LiteratureSource):
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def search(self, query: str, limit: int = 10) -> list[PaperRecord]:
        response = httpx.get(
            f"{self.BASE_URL}/esearch.fcgi",
            params={
                "db": "pubmed",
                "term": query,
                "retmode": "json",
                "retmax": limit,
            },
            timeout=30.0,
        )
        response.raise_for_status()

        ids = response.json()["esearchresult"]["idlist"]

        papers = []

        for pmid in ids:
            papers.append(
                PaperRecord(
                    paper_id=f"pubmed:{pmid}",
                    title=f"PubMed article {pmid}",
                    pmid=pmid,
                    source="pubmed",
                )
            )

        return papers