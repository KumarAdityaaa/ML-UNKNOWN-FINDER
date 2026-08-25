from unknown_finder.hypothesis.generator import generate_hypotheses
from unknown_finder.hypothesis.models import Hypothesis
from unknown_finder.hypothesis.report import format_hypothesis_report


class HypothesisService:
    def generate(
        self,
        concept_pairs: list[
            tuple[str, str] | tuple[str, str, list[str]]
        ],
    ) -> list[Hypothesis]:
        return generate_hypotheses(concept_pairs)

    def report(
        self,
        concept_pairs: list[
            tuple[str, str] | tuple[str, str, list[str]]
        ],
    ) -> str:
        hypotheses = self.generate(concept_pairs)
        return format_hypothesis_report(hypotheses)

    