from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.evidence.storage import EvidenceStore
import pytest

def test_evidence_store_round_trip(tmp_path):
    path = tmp_path / "evidence.json"
    store = EvidenceStore(path)

    claim = Claim(
        claim_id="paper-001-claim-001",
        text="The proposed method improved performance.",
        paper_id="paper-001",
        section="Results",
    )

    evidence = Evidence(
        evidence_id="paper-001-claim-001-evidence-001",
        claim_id=claim.claim_id,
        text=claim.text,
        paper_id="paper-001",
        evidence_type="supporting",
    )

    store.save([claim], [evidence])

    claims, loaded_evidence = store.load()

    assert claims == [claim]
    assert loaded_evidence == [evidence]

def test_evidence_store_returns_empty_lists_when_file_missing(tmp_path):
    path = tmp_path / "missing-evidence.json"
    store = EvidenceStore(path)

    claims, evidence = store.load()

    assert claims == []
    assert evidence == []

def test_evidence_store_preserves_claim_relationship(tmp_path):
    path = tmp_path / "evidence.json"
    store = EvidenceStore(path)

    claim = Claim(
        claim_id="claim-001",
        text="The method improves accuracy.",
        paper_id="paper-001",
        section="Results",
    )

    evidence = Evidence(
        evidence_id="evidence-001",
        claim_id="claim-001",
        text="The method improved accuracy by 5 percent.",
        paper_id="paper-001",
        evidence_type="supporting",
    )

    store.save([claim], [evidence])

    loaded_claims, loaded_evidence = store.load()

    claim_ids = {item.claim_id for item in loaded_claims}

    assert loaded_evidence[0].claim_id in claim_ids

def test_evidence_store_rejects_orphan_evidence(tmp_path):

    store = EvidenceStore(tmp_path / "evidence.json")

    evidence = Evidence(
        evidence_id="evidence-001",
        claim_id="missing-claim",
        text="Unsupported evidence.",
        paper_id="paper-001",
        evidence_type="supporting",
    )

    with pytest.raises(ValueError, match="unknown claim"):
        store.save([], [evidence])