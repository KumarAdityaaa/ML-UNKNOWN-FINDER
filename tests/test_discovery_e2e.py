import pytest

from unknown_finder.evaluation.ablation import evaluate_ablation
from unknown_finder.evaluation.human import HumanEvaluation
from unknown_finder.evaluation.human_service import average_human_score
from unknown_finder.evaluation.models import EvaluationCase, EvaluationDataset
from unknown_finder.evaluation.service import EvaluationService
from unknown_finder.gaps.detector import detect_gaps
from unknown_finder.hypothesis.service import HypothesisService


def test_discovery_to_evaluation_end_to_end():
    gaps = detect_gaps([
        ("attention", "medical imaging", 0.9),
    ])

    assert len(gaps) == 1

    hypotheses = HypothesisService().generate(gaps)

    assert len(hypotheses) == 1
    assert hypotheses[0].concept_a == "attention"
    assert hypotheses[0].concept_b == "medical imaging"

    dataset = EvaluationDataset([
        EvaluationCase(
            input_text="attention + medical imaging",
            expected="testable hypothesis",
            actual="testable hypothesis",
        )
    ])

    result = EvaluationService().evaluate(
        dataset,
        lambda case: 1.0 if case.actual == case.expected else 0.0,
    )

    assert result.metric == "dataset_score"
    assert result.score == 1.0

    human_score = average_human_score([
        HumanEvaluation(
            hypothesis="testable hypothesis",
            relevance=0.9,
            testability=0.8,
            novelty=0.7,
        )
    ])

    assert human_score == pytest.approx(0.8)

    ablation = evaluate_ablation(0.8, 0.6)
    assert ablation.score_difference == pytest.approx(-0.2)
