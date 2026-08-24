import json
from pathlib import Path

from .models import Claim, Evidence


class EvidenceStore:
    def __init__(self, path: str | Path = "data/metadata/evidence.json"):
        self.path = Path(path)

    def save(
        self,
        claims: list[Claim],
        evidence: list[Evidence],
    ) -> None:
        claim_ids = {claim.claim_id for claim in claims}

        for item in evidence:
            if item.claim_id not in claim_ids:
                raise ValueError(
                    f"Evidence {item.evidence_id!r} references "
                    f"unknown claim {item.claim_id!r}"
                )

        self.path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "claims": [
                claim.model_dump(mode="json")
                for claim in claims
            ],
            "evidence": [
                item.model_dump(mode="json")
                for item in evidence
            ],
        }

        self.path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def load(self) -> tuple[list[Claim], list[Evidence]]:
        if not self.path.exists():
            return [], []

        data = json.loads(
            self.path.read_text(encoding="utf-8")
        )

        claims = [
            Claim.model_validate(item)
            for item in data.get("claims", [])
        ]

        evidence = [
            Evidence.model_validate(item)
            for item in data.get("evidence", [])
        ]

        return claims, evidence