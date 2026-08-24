from unknown_finder.evidence.models import Claim
from unknown_finder.extraction.concepts import Concept


def link_claims_to_concepts(
    claims: list[Claim],
    concepts: list[Concept],
) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []

    for claim in claims:
        claim_text = claim.text.lower()

        for concept in concepts:
            if concept.term.lower() in claim_text:
                links.append(
                    (claim.claim_id, concept.term)
                )

    return links