from unknown_finder.hypothesis.generator import generate_hypotheses
from unknown_finder.hypothesis.models import Hypothesis
import pytest
from unknown_finder.gaps.models import Gap

def test_generate_hypothesis_from_gap():
    hypotheses = generate_hypotheses(
        [
            ("attention", "medical imaging"),
        ]
    )

    assert len(hypotheses) == 1

    hypothesis = hypotheses[0]

    assert isinstance(hypothesis, Hypothesis)
    assert hypothesis.concept_a == "attention"
    assert hypothesis.concept_b == "medical imaging"

def test_hypothesis_contains_evidence_trace():
    hypotheses = generate_hypotheses(
        [
            ("attention", "medical imaging"),
        ]
    )

    hypothesis = hypotheses[0]

    assert hypothesis.evidence_ids == []

def test_hypothesis_accepts_evidence_ids():
    hypothesis = Hypothesis(
        concept_a="attention",
        concept_b="medical imaging",
        evidence_ids=[
            "evidence-001",
            "evidence-002",
        ],
    )

    assert hypothesis.evidence_ids == [
        "evidence-001",
        "evidence-002",
    ]

def test_generate_hypothesis_with_evidence_ids():
    hypotheses = generate_hypotheses(
        [
            (
                "attention",
                "medical imaging",
                ["evidence-001", "evidence-002"],
            ),
        ]
    )

    assert len(hypotheses) == 1

    hypothesis = hypotheses[0]

    assert hypothesis.concept_a == "attention"
    assert hypothesis.concept_b == "medical imaging"
    assert hypothesis.evidence_ids == [
        "evidence-001",
        "evidence-002",
    ]

def test_generate_hypotheses_with_no_pairs_returns_empty():
    hypotheses = generate_hypotheses([])

    assert hypotheses == []

def test_hypothesis_rejects_empty_concept():

    with pytest.raises(ValueError):
        Hypothesis(
            concept_a="",
            concept_b="medical imaging",
        )

def test_hypothesis_rejects_empty_second_concept():

    with pytest.raises(ValueError):
        Hypothesis(
            concept_a="attention",
            concept_b="",
        )

def test_hypothesis_rejects_empty_evidence_id():

    with pytest.raises(ValueError):
        Hypothesis(
            concept_a="attention",
            concept_b="medical imaging",
            evidence_ids=["evidence-001", ""],
        )

def test_hypothesis_rejects_duplicate_evidence_ids():

    with pytest.raises(ValueError):
        Hypothesis(
            concept_a="attention",
            concept_b="medical imaging",
            evidence_ids=[
                "evidence-001",
                "evidence-001",
            ],
        )

def test_generate_hypotheses_from_gaps():
    gaps = [
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
        ),
    ]

    hypotheses = generate_hypotheses(gaps)

    assert len(hypotheses) == 1

    hypothesis = hypotheses[0]

    assert hypothesis.concept_a == "attention"
    assert hypothesis.concept_b == "medical imaging"
    assert hypothesis.evidence_ids == []

def test_generate_hypothesis_preserves_gap_confidence():
    gaps = [
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
            confidence=0.75,
        ),
    ]

    hypotheses = generate_hypotheses(gaps)

    assert len(hypotheses) == 1
    assert hypotheses[0].confidence == 0.75