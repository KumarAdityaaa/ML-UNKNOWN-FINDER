from unknown_finder.contradiction.detector import detect_contradictions
from unknown_finder.contradiction.models import Contradiction
from unknown_finder.evidence.models import Claim
from unknown_finder.contradiction.report import format_contradiction_report

class ContradictionService:
    def detect(
        self,
        claims: list[Claim],
    ) -> list[Contradiction]:
        return detect_contradictions(claims)

    def report(
        self,
        claims: list[Claim],
    ) -> str:
        contradictions = self.detect(claims)
        return format_contradiction_report(contradictions)

    