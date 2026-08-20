from dataclasses import dataclass

from .citation_stats import CitationStatistics
from .models import Reference


@dataclass
class ReferenceImpact:
    reference_id: str
    citation_count: int
    impact_score: float
    rank: int


def calculate_reference_impact(
    statistics: CitationStatistics,
    references: list[Reference],
) -> list[ReferenceImpact]:
    ranked = statistics.most_cited

    if not ranked:
        return [
            ReferenceImpact(
                reference_id=reference.reference_id,
                citation_count=0,
                impact_score=0.0,
                rank=0,
            )
            for reference in references
        ]

    maximum = ranked[0][1]

    rank_by_id = {
        reference_id: index + 1
        for index, (reference_id, _) in enumerate(ranked)
    }

    count_by_id = dict(ranked)

    impacts: list[ReferenceImpact] = []

    for reference in references:
        count = count_by_id.get(reference.reference_id, 0)

        score = (
            count / maximum
            if maximum > 0
            else 0.0
        )

        impacts.append(
            ReferenceImpact(
                reference_id=reference.reference_id,
                citation_count=count,
                impact_score=round(score, 4),
                rank=rank_by_id.get(reference.reference_id, 0),
            )
        )

    return impacts