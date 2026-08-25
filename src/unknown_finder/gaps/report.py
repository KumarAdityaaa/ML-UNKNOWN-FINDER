from unknown_finder.gaps.models import Gap


def format_gap_report(
    gaps: list[Gap],
    limit: int | None = None,
) -> str:
    lines = [
        "Research Gaps",
        "=============",
    ]

    if not gaps:
        lines.append("No research gaps detected.")
        return "\n".join(lines)
    if limit is not None:
        gaps = gaps[:limit]
        
    for index, gap in enumerate(gaps, start=1):
        lines.append(
            f"{index}. {gap.concept_a} "
            f"<-> {gap.concept_b} "
            f"(confidence={gap.confidence:.4f})"
        )

    return "\n".join(lines)