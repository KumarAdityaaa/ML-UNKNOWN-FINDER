from unknown_finder.contradiction.detector import detect_contradictions
from unknown_finder.contradiction.models import Contradiction
from unknown_finder.contradiction.service import ContradictionService
from unknown_finder.evidence.models import Claim


def test_contradiction_service_detects_claim_conflicts():
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

    service = ContradictionService()

    contradictions = service.detect(claims)

    assert len(contradictions) == 1
    assert isinstance(contradictions[0], Contradiction)
    assert contradictions[0].claim_a == "claim-001"
    assert contradictions[0].claim_b == "claim-002"

def test_contradiction_service_formats_report():
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

    service = ContradictionService()

    report = service.report(claims)

    assert "Contradictions" in report
    assert "claim-001" in report
    assert "claim-002" in report
    assert "paper-001" in report
    assert "paper-002" in report

def test_contradiction_service_empty_report():
    service = ContradictionService()

    report = service.report([])

    assert report == (
        "Contradictions\n"
        "==============\n"
        "No contradictions detected."
    )

def test_contradiction_service_detect_empty_claims():
    service = ContradictionService()

    contradictions = service.detect([])

    assert contradictions == []

def test_contradiction_service_report_preserves_paper_traceability():
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

    service = ContradictionService()

    report = service.report(claims)

    assert "claim-001" in report
    assert "claim-002" in report
    assert "paper-001" in report
    assert "paper-002" in report