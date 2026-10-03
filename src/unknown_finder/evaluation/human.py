from dataclasses import dataclass


@dataclass(frozen=True)
class HumanEvaluation:
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
                raise ValueError("human evaluation scores must be between 0.0 and 1.0")

    @property
    def quality_score(self) -> float:
        return (self.relevance + self.testability + self.novelty) / 3
