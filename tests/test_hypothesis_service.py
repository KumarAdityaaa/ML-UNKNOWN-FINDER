from unknown_finder.hypothesis.models import Hypothesis
from unknown_finder.hypothesis.service import HypothesisService


def test_hypothesis_service_generates_hypotheses():
    service = HypothesisService()

    hypotheses = service.generate(
        [
            ("attention", "medical imaging"),
        ]
    )

    assert len(hypotheses) == 1

    hypothesis = hypotheses[0]

    assert isinstance(hypothesis, Hypothesis)
    assert hypothesis.concept_a == "attention"
    assert hypothesis.concept_b == "medical imaging"

def test_hypothesis_service_formats_report():
    service = HypothesisService()

    report = service.report(
        [
            (
                "attention",
                "medical imaging",
                ["evidence-001"],
            ),
        ]
    )

    assert "Hypotheses" in report
    assert "attention" in report
    assert "medical imaging" in report
    assert "evidence-001" in report

def test_hypothesis_service_empty_input():
    service = HypothesisService()

    hypotheses = service.generate([])

    assert hypotheses == []


def test_hypothesis_service_empty_report():
    service = HypothesisService()

    report = service.report([])

    assert report == (
        "Hypotheses\n"
        "==========\n"
        "No hypotheses generated."
    )

def test_hypothesis_service_preserves_evidence_ids():
    service = HypothesisService()

    hypotheses = service.generate(
        [
            (
                "attention",
                "medical imaging",
                ["evidence-001", "evidence-002"],
            ),
        ]
    )

    assert len(hypotheses) == 1
    assert hypotheses[0].evidence_ids == [
        "evidence-001",
        "evidence-002",
    ]

    report = service.report(
        [
            (
                "attention",
                "medical imaging",
                ["evidence-001", "evidence-002"],
            ),
        ]
    )

    assert "evidence-001" in report
    assert "evidence-002" in report