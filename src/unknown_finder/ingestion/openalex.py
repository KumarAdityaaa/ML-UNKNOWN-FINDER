from .base import LiteratureSource
from .models import PaperRecord


class OpenAlexSource(LiteratureSource):

    def search(self, query: str, limit: int = 10) -> list[PaperRecord]:
        raise NotImplementedError