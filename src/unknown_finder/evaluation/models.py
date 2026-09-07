from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationResult:
    metric: str
    score: float
