from unknown_finder.evidence.models import Claim, Evidence
import pytest

def test_claim_and_evidence_models():
    claim = Claim(
        claim_id="claim-001",
        text="Self-attention reduces maximum path length.",
        paper_id="1706.03762",
        section="Why Self-Attention",
    )

    evidence = Evidence(
        evidence_id="evidence-001",
        claim_id="claim-001",
        text="Self-attention connects all positions with a constant number of operations.",
        paper_id="1706.03762",
        evidence_type="supporting",
    )

    assert claim.claim_id == "claim-001"
    assert claim.paper_id == "1706.03762"
    assert evidence.claim_id == claim.claim_id
    assert evidence.evidence_type == "supporting"

def test_claim_requires_required_fields():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Claim(
            claim_id="claim-001",
            text="Some claim",
            paper_id="1706.03762",
        )


def test_evidence_requires_claim_id():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="evidence-001",
            text="Supporting evidence",
            paper_id="1706.03762",
            evidence_type="supporting",
        )

def test_evidence_rejects_invalid_evidence_type():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="evidence-001",
            claim_id="claim-001",
            text="Some evidence",
            paper_id="1706.03762",
            evidence_type="unknown-type",
        )