from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationResult:
    metric: str
    score: float


@dataclass(frozen=True)
class EvaluationCase:
    input_text: str
    expected: str
    actual: str | None = None
