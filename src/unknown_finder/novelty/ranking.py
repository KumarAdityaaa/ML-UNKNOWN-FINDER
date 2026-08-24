from dataclasses import dataclass

from unknown_finder.extraction.novelty import NoveltyResult
from unknown_finder.ingestion.models import PaperRecord


@dataclass
class RankedUnknown:
    term: str
    novelty_score: float
    reason: str
    paper_id: str
    paper_title: str


def rank_unknowns(
    papers: list[PaperRecord],
) -> list[RankedUnknown]:
    best_results: dict[str, RankedUnknown] = {}

    for paper in papers:
        for result in paper.novelty_results:
            existing = best_results.get(result.term)

            ranked = RankedUnknown(
                term=result.term,
                novelty_score=result.novelty_score,
                reason=result.reason,
                paper_id=paper.paper_id,
                paper_title=paper.title,
            )

            if (
                existing is None
                or ranked.novelty_score > existing.novelty_score
            ):
                best_results[result.term] = ranked

    results = list(best_results.values())

    results.sort(
        key=lambda result: (
            -result.novelty_score,
            result.term,
        )
    )

    return results