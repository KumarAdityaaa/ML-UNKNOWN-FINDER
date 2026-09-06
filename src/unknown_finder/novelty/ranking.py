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

            if existing is not None:
                if paper.paper_id not in existing.source_paper_ids:
                    existing.source_paper_ids.append(paper.paper_id)

                if result.novelty_score <= existing.novelty_score:
                    continue

            best_results[result.term] = RankedUnknown(
                term=result.term,
                novelty_score=result.novelty_score,
                reason=result.reason,
                paper_id=paper.paper_id,
                paper_title=paper.title,
                source_paper_ids=(
                    existing.source_paper_ids
                    if existing is not None
                    else [paper.paper_id]
                ),
            )

    results = list(best_results.values())

    results.sort(
        key=lambda result: (
            -result.novelty_score,
            result.term,
        )
    )

    return results
