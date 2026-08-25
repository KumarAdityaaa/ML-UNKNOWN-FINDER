from dataclasses import dataclass, field

from unknown_finder.contradiction.models import Contradiction
from unknown_finder.gaps.models import Gap
from unknown_finder.hypothesis.models import Hypothesis


@dataclass
class AnalysisResult:
    contradictions: list[Contradiction] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    hypotheses: list[Hypothesis] = field(default_factory=list)

    @property
    def contradiction_count(self) -> int:
        return len(self.contradictions)

    @property
    def gap_count(self) -> int:
        return len(self.gaps)

    @property
    def hypothesis_count(self) -> int:
        return len(self.hypotheses)