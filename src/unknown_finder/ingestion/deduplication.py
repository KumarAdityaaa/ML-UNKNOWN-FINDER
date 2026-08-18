from .models import PaperRecord


def _deduplication_key(paper: PaperRecord) -> str:
    if paper.doi:
        return f"doi:{paper.doi.lower()}"

    if paper.arxiv_id:
        return f"arxiv:{paper.arxiv_id.lower()}"

    if paper.pmid:
        return f"pmid:{paper.pmid}"

    return f"id:{paper.paper_id}"


def deduplicate(papers: list[PaperRecord]) -> list[PaperRecord]:
    seen = set()
    unique = []

    for paper in papers:
        key = _deduplication_key(paper)

        if key not in seen:
            seen.add(key)
            unique.append(paper)

    return unique