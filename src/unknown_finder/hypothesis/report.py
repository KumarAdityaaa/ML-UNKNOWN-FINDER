from unknown_finder.hypothesis.models import Hypothesis


def format_hypothesis_report(
    hypotheses: list[Hypothesis],
    limit: int | None = None,
) -> str:
    lines = [
        "Hypotheses",
        "==========",
    ]

    if not hypotheses:
        lines.append("No hypotheses generated.")
        return "\n".join(lines)
    if limit is not None:
        hypotheses = hypotheses[:limit]
        
    for index, hypothesis in enumerate(
        hypotheses,
        start=1,
    ):
        lines.append(
            f"{index}. {hypothesis.concept_a} "
            f"<-> {hypothesis.concept_b}"
        )

        if hypothesis.evidence_ids:
            lines.append(
                "   Evidence: "
                + ", ".join(hypothesis.evidence_ids)
            )
        else:
            lines.append("   Evidence: none")

    return "\n".join(lines)