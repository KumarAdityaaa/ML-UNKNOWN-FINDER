from .ranking import RankedUnknown


def format_unknown_report(
    results: list[RankedUnknown],
    limit: int | None = None,
) -> str:
    selected = results if limit is None else results[:limit]

    if not selected:
        return "No unknowns found."

    lines = ["Unknown Concepts", "================="]

    for index, result in enumerate(selected, start=1):
        lines.append(
            f"{index}. {result.term} "
            f"(score={result.novelty_score:.4f})"
        )
        lines.append(f"   Reason: {result.reason}")
        lines.append(
            f"   Paper: {result.paper_title} "
            f"[{result.paper_id}]"
        )
        lines.append(
            f"   Sources: {len(result.source_paper_ids)} paper(s)"
        )

    return "\n".join(lines)