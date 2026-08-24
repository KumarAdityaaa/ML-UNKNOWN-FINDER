from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.parsing.models import DocumentSection


def extract_evidence(
    claim: Claim,
    sections: list[DocumentSection],
) -> list[Evidence]:
    for section in sections:
        if section.heading != claim.section:
            continue

        if claim.text not in section.text:
            return []

        return [
            Evidence(
                evidence_id=f"{claim.claim_id}-evidence-001",
                claim_id=claim.claim_id,
                text=claim.text,
                paper_id=claim.paper_id,
                evidence_type="supporting",
            )
        ]

    return []