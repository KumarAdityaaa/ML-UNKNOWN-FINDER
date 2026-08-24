from unknown_finder.extraction.novelty import NoveltyResult
from unknown_finder.ingestion.models import PaperRecord


def rank_unknowns(
    papers: list[PaperRecord],
) -> list[NoveltyResult]:
    best_results: dict[str, NoveltyResult] = {}

    for paper in papers:
        for result in paper.novelty_results:
            existing = best_results.get(result.term)

            if existing is None or result.novelty_score > existing.novelty_score:
                best_results[result.term] = result

    results = list(best_results.values())

    results.sort(
        key=lambda result: (
            -result.novelty_score,
            result.term,
        )
    )

    return results