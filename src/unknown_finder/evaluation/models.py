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

    @property
    def quality_score(self) -> float:
        return (self.relevance + self.testability + self.novelty) / 3