from pathlib import Path

from unknown_finder.evaluation.ablation import evaluate_ablation
from unknown_finder.evaluation.human import HumanEvaluation
from unknown_finder.evaluation.human_service import average_human_score
from unknown_finder.evaluation.models import EvaluationCase, EvaluationDataset
from unknown_finder.evaluation.service import EvaluationService
from unknown_finder.gaps.detector import detect_gaps
from unknown_finder.hypothesis.service import HypothesisService


def build_dashboard() -> str:
    gaps = detect_gaps([
        ("attention", "medical imaging", 0.9),
    ])
    hypotheses = HypothesisService().generate(gaps)

    dataset = EvaluationDataset([
        EvaluationCase(
            input_text="attention + medical imaging",
            expected="testable hypothesis",
            actual="testable hypothesis",
        )
    ])

    evaluation = EvaluationService().evaluate(
        dataset,
        lambda case: 1.0 if case.actual == case.expected else 0.0,
    )

    human_score = average_human_score([
        HumanEvaluation(
            hypothesis="testable hypothesis",
            relevance=0.9,
            testability=0.8,
            novelty=0.7,
        )
    ])

    ablation = evaluate_ablation(0.8, 0.6)

    hypothesis_rows = "".join(
        f"<li>{hypothesis.concept_a} ? {hypothesis.concept_b}</li>"
        for hypothesis in hypotheses
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI Unknown Finder Dashboard</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; line-height: 1.5; }}
.card {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 16px 0; }}
.metric {{ font-size: 2rem; font-weight: bold; }}
</style>
</head>
<body>
<h1>AI Unknown Finder Dashboard</h1>

<div class="card">
<h2>Discovery</h2>
<p>Detected gaps: <span class="metric">{len(gaps)}</span></p>
<ul>{hypothesis_rows}</ul>
</div>

<div class="card">
<h2>Evaluation</h2>
<p>Dataset score: <span class="metric">{evaluation.score:.2f}</span></p>
<p>Human evaluation score: <span class="metric">{human_score:.2f}</span></p>
<p>Ablation difference: <span class="metric">{ablation.score_difference:.2f}</span></p>
</div>
</body>
</html>
"""


def main() -> None:
    output = Path("dashboard") / "index.html"
    output.write_text(build_dashboard(), encoding="utf-8")
    print(f"Dashboard generated: {output}")


if __name__ == "__main__":
    main()
