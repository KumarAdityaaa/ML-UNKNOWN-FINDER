from .models import PaperRecord


def deduplicate(papers: list[PaperRecord]) -> list[PaperRecord]:
    seen = set()
    unique = []

    for paper in papers:
        if paper.paper_id not in seen:
            seen.add(paper.paper_id)
            unique.append(paper)

    return unique