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

    contradiction = contradictions[0]

    assert contradiction.claim_a == "claim-001"
    assert contradiction.claim_b == "claim-002"
    assert contradiction.paper_a == "paper-001"
    assert contradiction.paper_b == "paper-002"

def test_detect_contradictions_preserves_paper_pairing_in_reverse_order():
    claims = [
        Claim(
            claim_id="claim-002",
            text="The proposed method does not improve accuracy.",
            paper_id="paper-002",
            section="Results",
        ),
        Claim(
            claim_id="claim-001",
            text="The proposed method improves accuracy.",
            paper_id="paper-001",
            section="Results",
        ),
    ]

    contradictions = detect_contradictions(claims)

    assert len(contradictions) == 1

    contradiction = contradictions[0]

    assert contradiction.claim_a == "claim-002"
    assert contradiction.claim_b == "claim-001"
    assert contradiction.paper_a == "paper-002"
    assert contradiction.paper_b == "paper-001"