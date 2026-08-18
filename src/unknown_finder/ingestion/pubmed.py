import httpx

from .base import LiteratureSource
from .models import PaperRecord


class PubMedSource(LiteratureSource):
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def search(self, query: str, limit: int = 10) -> list[PaperRecord]:
        raise NotImplementedError