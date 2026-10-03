from dataclasses import dataclass


@dataclass(frozen=True)
class AblationResult:
    baseline_score: float
    ablated_score: float

    def __post_init__(self) -> None:
        for score in (self.baseline_score, self.ablated_score):
            if not 0.0 <= score <= 1.0:
                raise ValueError("ablation scores must be between 0.0 and 1.0")

    @property
    def score_difference(self) -> float:
        return self.ablated_score - self.baseline_score


def evaluate_ablation(
    baseline_score: float,
    ablated_score: float,
) -> AblationResult:
    return AblationResult(
        baseline_score=baseline_score,
        ablated_score=ablated_score,
    )
