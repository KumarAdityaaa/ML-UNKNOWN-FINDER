from collections import Counter
from dataclasses import dataclass

from .models import Citation, Reference


@dataclass
class CitationStatistics:
    total_citations: int
    unique_citations: int
    citation_frequency: dict[str, int]
    most_cited: list[tuple[str, int]]
    uncited_references: list[str]


def calculate_citation_statistics(
    citations: list[Citation],
    references: list[Reference],
) -> CitationStatistics:
    frequency = Counter(
        citation.reference_id
        for citation in citations
    )

    reference_ids = {
        reference.reference_id
        for reference in references
    }

    uncited = sorted(
        reference_ids - set(frequency),
        key=int,
    )

    most_cited = sorted(
        frequency.items(),
        key=lambda item: (-item[1], int(item[0])),
    )

    return CitationStatistics(
        total_citations=len(citations),
        unique_citations=len(frequency),
        citation_frequency=dict(frequency),
        most_cited=most_cited,
        uncited_references=uncited,
    )