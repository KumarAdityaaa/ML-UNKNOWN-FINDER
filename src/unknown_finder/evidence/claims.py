import re

from unknown_finder.evidence.models import Claim
from unknown_finder.parsing.models import DocumentSection


def extract_claims(
    paper_id: str,
    sections: list[DocumentSection],
) -> list[Claim]:
    claims: list[Claim] = []
    claim_number = 1

    for section in sections:
        sentences = re.split(r"(?<=[.!?])\s+", section.text.strip())

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            if not sentence.endswith((".", "!", "?")):
                continue

            claims.append(
                Claim(
                    claim_id=f"{paper_id}-claim-{claim_number:03d}",
                    text=sentence,
                    paper_id=paper_id,
                    section=section.heading,
                )
            )

            claim_number += 1

    return claims