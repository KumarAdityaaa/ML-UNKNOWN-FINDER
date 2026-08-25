from dataclasses import dataclass, field


@dataclass
class Hypothesis:
    concept_a: str
    concept_b: str
    evidence_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.concept_a.strip():
            raise ValueError("concept_a must not be empty")

        if not self.concept_b.strip():
            raise ValueError("concept_b must not be empty")

        if any(
            not evidence_id.strip()
            for evidence_id in self.evidence_ids
        ):
            raise ValueError(
                "evidence_ids must not contain empty IDs"
            )

        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError(
                "evidence_ids must be unique"
            )