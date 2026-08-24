from unknown_finder.evidence.models import Claim
from unknown_finder.contradiction.detector import detect_contradictions


def test_detect_contradictory_claims():
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

    contradictions = detect_contradictions(claims)

    assert len(contradictions) == 1
    assert contradictions[0].claim_a == "claim-001"
    assert contradictions[0].claim_b == "claim-002"

def test_detect_contradictions_is_order_independent():
    claims = [
        Claim(
            claim_id="claim-001",
            text="The proposed method does not improve accuracy.",
            paper_id="paper-001",
            section="Results",
        ),
        Claim(
            claim_id="claim-002",
            text="The proposed method improves accuracy.",
            paper_id="paper-002",
            section="Results",
        ),
    ]

    contradictions = detect_contradictions(claims)

    assert len(contradictions) == 1
    assert contradictions[0].claim_a == "claim-001"
    assert contradictions[0].claim_b == "claim-002"

def test_detect_contradictions_ignores_matching_positive_claims():
    claims = [
        Claim(
            claim_id="claim-001",
            text="The proposed method improves accuracy.",
            paper_id="paper-001",
            section="Results",
        ),
        Claim(
            claim_id="claim-002",
            text="The proposed method improves accuracy.",
            paper_id="paper-002",
            section="Results",
        ),
    ]

    contradictions = detect_contradictions(claims)

    assert contradictions == []

def test_detect_contradictions_does_not_duplicate_pairs():
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
        Claim(
            claim_id="claim-003",
            text="The proposed method improves accuracy.",
            paper_id="paper-003",
            section="Results",
        ),
    ]

    contradictions = detect_contradictions(claims)

    pairs = {
        (item.claim_a, item.claim_b)
        for item in contradictions
    }

    assert len(contradictions) == len(pairs)