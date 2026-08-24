from dataclasses import dataclass

from unknown_finder.ingestion.models import PaperRecord


@dataclass
class RankedUnknown:
    term: str
    novelty_score: float
    reason: str
    paper_id: str
    paper_title: str
    source_paper_ids: list[str]


def rank_unknowns(
    papers: list[PaperRecord],
) -> list[RankedUnknown]:
    best_results: dict[str, RankedUnknown] = {}

    for paper in papers:
        for result in paper.novelty_results:
            existing = best_results.get(result.term)

            if existing is None:
                best_results[result.term] = RankedUnknown(
                    term=result.term,
                    novelty_score=result.novelty_score,
                    reason=result.reason,
                    paper_id=paper.paper_id,
                    paper_title=paper.title,
                    source_paper_ids=[paper.paper_id],
                )
                continue

            if paper.paper_id not in existing.source_paper_ids:
                existing.source_paper_ids.append(paper.paper_id)

            if result.novelty_score > existing.novelty_score:
                existing.term = result.term
                existing.novelty_score = result.novelty_score
                existing.reason = result.reason
                existing.paper_id = paper.paper_id
                existing.paper_title = paper.title

    results = list(best_results.values())

    results.sort(
        key=lambda result: (
            -result.novelty_score,
            result.term,
        )
    )

    return results