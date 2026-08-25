from unknown_finder.analysis.builder import build_analysis_result
from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.extraction.concepts import Concept
import pytest

def test_build_analysis_result_from_claims_evidence_and_concepts():
    claims = [
        Claim(
            claim_id="claim-001",
            text="The proposed method improves accuracy.",
            paper_id="paper-001",
            section="Results",
        ),
        Claim(
            claim_id="claim-002",
            text="The proposed method does not improve accuracy.",
            paper_id="paper-002",
            section="Results",
        ),
    ]

    evidence = [
        Evidence(
            evidence_id="evidence-001",
            claim_id="claim-001",
            text="Accuracy improved.",
            paper_id="paper-001",
            evidence_type="supporting",
        ),
    ]

    concepts = [
        Concept(
            term="accuracy",
            frequency=2,
            sections=["Results"],
            contexts=["accuracy improved"],
            score=1.0,
        ),
    ]

    result = build_analysis_result(
        claims=claims,
        evidence=evidence,
        concepts=concepts,
    )

    assert result.contradiction_count == 1
    assert result.gap_count == 0
    assert result.hypothesis_count == 0

    assert len(result.contradictions) == 1
def test_build_analysis_result_from_candidate_pairs():
    result = build_analysis_result(
        claims=[],
        evidence=[],
        concepts=[],
        candidate_pairs=[
            ("attention", "medical imaging"),
        ],
    )

    assert result.gap_count == 1
    assert result.hypothesis_count == 1

    assert result.gaps[0].concept_a == "attention"
    assert result.gaps[0].concept_b == "medical imaging"

    assert result.hypotheses[0].concept_a == "attention"
    assert result.hypotheses[0].concept_b == "medical imaging"

def test_build_analysis_result_preserves_gap_confidence_in_hypothesis():
    result = build_analysis_result(
        claims=[],
        evidence=[],
        concepts=[],
        candidate_pairs=[
            ("attention", "medical imaging"),
        ],
    )

    assert result.gap_count == 1
    assert result.hypothesis_count == 1

    assert result.gaps[0].confidence == 1.0
    assert result.hypotheses[0].confidence == 1.0

def test_build_analysis_result_uses_candidate_pair_confidence():
    result = build_analysis_result(
        claims=[],
        evidence=[],
        concepts=[],
        candidate_pairs=[
            ("attention", "medical imaging", 0.75),
        ],
    )

    assert result.gap_count == 1
    assert result.hypothesis_count == 1
    assert result.gaps[0].confidence == 0.75
    assert result.hypotheses[0].confidence == 0.75

def test_build_analysis_result_rejects_invalid_candidate_pair_confidence():

    with pytest.raises(ValueError):
        build_analysis_result(
            claims=[],
            evidence=[],
            concepts=[],
            candidate_pairs=[
                ("attention", "medical imaging", 1.5),
            ],
        )

def test_build_analysis_result_rejects_negative_candidate_pair_confidence():

    with pytest.raises(ValueError):
        build_analysis_result(
            claims=[],
            evidence=[],
            concepts=[],
            candidate_pairs=[
                ("attention", "medical imaging", -0.1),
            ],
        )

def test_build_analysis_result_accepts_confidence_boundaries():
    result = build_analysis_result(
        claims=[],
        evidence=[],
        concepts=[],
        candidate_pairs=[
            ("attention", "medical imaging", 0.0),
            ("transformer", "genomics", 1.0),
        ],
    )

    assert result.gap_count == 2
    assert result.hypothesis_count == 2

    assert result.gaps[0].confidence == 0.0
    assert result.gaps[1].confidence == 1.0

    assert result.hypotheses[0].confidence == 0.0
    assert result.hypotheses[1].confidence == 1.0

def test_build_analysis_result_preserves_highest_gap_confidence():
    result = build_analysis_result(
        claims=[],
        evidence=[],
        concepts=[],
        candidate_pairs=[
            ("attention", "medical imaging", 0.4),
            ("medical imaging", "attention", 0.9),
        ],
    )

    assert result.gap_count == 1
    assert result.hypothesis_count == 1

    assert result.gaps[0].confidence == 0.9
    assert result.hypotheses[0].confidence == 0.9

def test_build_analysis_result_complete_phase4_pipeline():
    claims = [
        Claim(
            claim_id="claim-001",
            text="The proposed method improves accuracy.",
            paper_id="paper-001",
            section="Results",
        ),
        Claim(
            claim_id="claim-002",
            text="The proposed method does not improve accuracy.",
            paper_id="paper-002",
            section="Results",
        ),
    ]

    evidence = [
        Evidence(
            evidence_id="evidence-001",
            claim_id="claim-001",
            text="Accuracy improved.",
            paper_id="paper-001",
            evidence_type="supporting",
        ),
    ]

    result = build_analysis_result(
        claims=claims,
        evidence=evidence,
        concepts=[],
        candidate_pairs=[
            ("attention", "medical imaging", 0.75),
        ],
    )

    assert result.contradiction_count == 1
    assert result.gap_count == 1
    assert result.hypothesis_count == 1

    assert result.contradictions[0].claim_a == "claim-001"
    assert result.contradictions[0].claim_b == "claim-002"

    assert result.gaps[0].confidence == 0.75

    assert result.hypotheses[0].concept_a == "attention"
    assert result.hypotheses[0].concept_b == "medical imaging"
    assert result.hypotheses[0].confidence == 0.75