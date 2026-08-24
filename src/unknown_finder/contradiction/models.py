from dataclasses import dataclass


@dataclass
class Contradiction:
    claim_a: str
    claim_b: str