from unknown_finder.evidence.claims import extract_claims
from unknown_finder.parsing.models import DocumentSection


def test_extract_claims_from_sections():
    sections = [
        DocumentSection(
            heading="Results",
            text=(
                "The proposed method improved performance. "
                "The model achieved higher accuracy than the baseline."
            ),
        ),
    ]

    claims = extract_claims(
        paper_id="paper-001",
        sections=sections,
    )

    assert len(claims) == 2
    assert claims[0].paper_id == "paper-001"
    assert claims[0].section == "Results"
    assert claims[0].text == "The proposed method improved performance."

def test_extract_claims_ignores_empty_and_incomplete_sentences():
    sections = [
        DocumentSection(
            heading="Methods",
            text=(
                "We collected data from three datasets. "
                "The evaluation used five metrics"
            ),
        ),
    ]

    claims = extract_claims(
        paper_id="paper-002",
        sections=sections,
    )

    assert len(claims) == 1
    assert claims[0].text == "We collected data from three datasets."


def test_extract_claims_preserves_section_boundaries():
    sections = [
        DocumentSection(
            heading="Introduction",
            text="Self-attention connects all positions.",
        ),
        DocumentSection(
            heading="Results",
            text="The proposed model improved accuracy.",
        ),
    ]

    claims = extract_claims(
        paper_id="paper-003",
        sections=sections,
    )

    assert len(claims) == 2
    assert claims[0].section == "Introduction"
    assert claims[1].section == "Results"
    assert claims[0].claim_id == "paper-003-claim-001"
    assert claims[1].claim_id == "paper-003-claim-002"