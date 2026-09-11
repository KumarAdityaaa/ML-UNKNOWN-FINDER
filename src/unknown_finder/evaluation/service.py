from collections.abc import Callable

from unknown_finder.evaluation.models import (
    EvaluationCase,
    EvaluationDataset,
    EvaluationResult,
)


class EvaluationService:
    def evaluate(
        self,
        dataset: EvaluationDataset,
        scorer: Callable[[EvaluationCase], float],
    ) -> EvaluationResult:
        if dataset.size == 0:
            return EvaluationResult(
                metric="dataset_score",
                score=0.0,
            )

        scores = [
            scorer(case)
            for case in dataset.cases
        ]

        return EvaluationResult(
            metric="dataset_score",
            score=sum(scores) / len(scores),
        )

    def compare(
        self,
        dataset: EvaluationDataset,
        baseline_scorer: Callable[[EvaluationCase], float],
        candidate_scorer: Callable[[EvaluationCase], float],
    ) -> EvaluationResult:
        baseline = self.evaluate(
            dataset,
            baseline_scorer,
        )
        candidate = self.evaluate(
            dataset,
            candidate_scorer,
        )

        return EvaluationResult(
            metric="candidate_minus_baseline",
            score=candidate.score - baseline.score,
        )