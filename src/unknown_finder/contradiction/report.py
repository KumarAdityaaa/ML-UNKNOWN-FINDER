from unknown_finder.contradiction.models import Contradiction


def format_contradiction_report(
    contradictions: list[Contradiction],
) -> str:
    lines = [
        "Contradictions",
        "==============",
    ]
    if not contradictions:
        lines.append("No contradictions detected.")
        return "\n".join(lines)

    for index, contradiction in enumerate(
        contradictions,
        start=1,
    ):
        lines.append(
            f"{index}. {contradiction.claim_a} "
            f"vs {contradiction.claim_b} "
            f"(confidence={contradiction.confidence:.4f})"
        )
        lines.append(
            f"   Paper A: {contradiction.paper_a}"
        )
        lines.append(
            f"   Paper B: {contradiction.paper_b}"
        )

    return "\n".join(lines)