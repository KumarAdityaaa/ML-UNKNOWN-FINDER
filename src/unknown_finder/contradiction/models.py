from dataclasses import dataclass


@dataclass
class Contradiction:
    claim_a: str
    claim_b: str
    paper_a: str
    paper_b: str
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "confidence must be between 0.0 and 1.0"
            )