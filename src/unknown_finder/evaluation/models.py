from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvaluationResult:
    metric: str
    score: float


@dataclass(frozen=True)
class EvaluationCase:
    input_text: str
    expected: str
    actual: str | None = None


@dataclass(frozen=True)
class EvaluationDataset:
    cases: list[EvaluationCase] = field(default_factory=list)

    @property
    def size(self) -> int:
        return len(self.cases)

@dataclass(frozen=True)
class HypothesisEvaluation:
    hypothesis: str
    relevance: float
    testability: float
    novelty: float

    def __post_init__(self) -> None:
        for score in (
            self.relevance,
            self.testability,
            self.novelty,
        ):
            if not 0.0 <= score <= 1.0:
                raise ValueError("evaluation scores must be between 0.0 and 1.0")

    @property
    def quality_score(self) -> float:
        return (self.relevance + self.testability + self.novelty) / 3
