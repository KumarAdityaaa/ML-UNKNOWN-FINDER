from unknown_finder.analysis.models import AnalysisResult
from unknown_finder.contradiction.detector import detect_contradictions
from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.extraction.concepts import Concept
from unknown_finder.gaps.detector import detect_gaps
from unknown_finder.hypothesis.generator import generate_hypotheses
from unknown_finder.knowledge_graph.builder import build_knowledge_graph


def build_analysis_result(
    claims: list[Claim],
    evidence: list[Evidence],
    concepts: list[Concept] | None = None,
    candidate_pairs: list[
    tuple[str, str] | tuple[str, str, float]
] | None = None,
) -> AnalysisResult:
    build_knowledge_graph(
        claims=claims,
        evidence=evidence,
        concepts=concepts,
    )

    contradictions = detect_contradictions(claims)

    gaps = detect_gaps(candidate_pairs or [])

    hypotheses = generate_hypotheses(gaps)

    return AnalysisResult(
        contradictions=contradictions,
        gaps=gaps,
        hypotheses=hypotheses,
    )