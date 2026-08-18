from abc import ABC, abstractmethod

from .models import PaperRecord


class LiteratureSource(ABC):

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> list[PaperRecord]:
        """Search the literature source and return normalized paper records."""
        raise NotImplementedError