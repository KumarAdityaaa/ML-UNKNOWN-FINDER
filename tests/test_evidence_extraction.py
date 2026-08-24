from unknown_finder.evidence.evidence import extract_evidence
from unknown_finder.evidence.models import Claim
from unknown_finder.parsing.models import DocumentSection


def test_extract_evidence_from_claim_source_section():
    sections = [
        DocumentSection(
            heading="Results",
            text=(
                "The proposed method improved performance. "
                "The model achieved higher accuracy than the baseline."
            ),
        ),
    ]

    claim = Claim(
        claim_id="paper-001-claim-001",
        text="The proposed method improved performance.",
        paper_id="paper-001",
        section="Results",
    )

    evidence = extract_evidence(
        claim=claim,
        sections=sections,
    )

    assert len(evidence) == 1
    assert evidence[0].claim_id == claim.claim_id
    assert evidence[0].paper_id == "paper-001"
    assert evidence[0].text == claim.text
    assert evidence[0].evidence_type == "supporting"

def test_extract_evidence_returns_empty_when_claim_not_in_section():
    sections = [
        DocumentSection(
            heading="Results",
            text="The baseline achieved 80 percent accuracy.",
        ),
    ]

    claim = Claim(
        claim_id="paper-002-claim-001",
        text="The proposed method achieved 95 percent accuracy.",
        paper_id="paper-002",
        section="Results",
    )

    evidence = extract_evidence(
        claim=claim,
        sections=sections,
    )

    assert evidence == []