from unknown_finder.analysis.models import AnalysisResult
from unknown_finder.contradiction.models import Contradiction
from unknown_finder.gaps.models import Gap
from unknown_finder.hypothesis.models import Hypothesis


def test_analysis_result_contains_phase4_outputs():
    result = AnalysisResult(
        contradictions=[
            Contradiction(
                claim_a="claim-001",
                claim_b="claim-002",
                paper_a="paper-001",
                paper_b="paper-002",
            ),
            Contradiction(
                claim_a="claim-003",
                claim_b="claim-004",
                paper_a="paper-003",
                paper_b="paper-004",
            ),
        ],
        gaps=[
            Gap("attention", "medical imaging"),
            Gap("transformer", "genomics"),
            Gap("vision", "robotics"),
        ],
        hypotheses=[
            Hypothesis("attention", "medical imaging"),
            Hypothesis("transformer", "genomics"),
            Hypothesis("vision", "robotics"),
            Hypothesis("language", "robotics"),
        ],
    )

    assert result.contradiction_count == 2
    assert result.gap_count == 3
    assert result.hypothesis_count == 4


def test_analysis_result_contains_phase4_objects():
    contradiction = Contradiction(
        claim_a="claim-001",
        claim_b="claim-002",
        paper_a="paper-001",
        paper_b="paper-002",
    )

    gap = Gap(
        concept_a="attention",
        concept_b="medical imaging",
        confidence=0.75,
    )

    hypothesis = Hypothesis(
        concept_a="attention",
        concept_b="medical imaging",
        evidence_ids=["evidence-001"],
        confidence=0.75,
    )

    result = AnalysisResult(
        contradictions=[contradiction],
        gaps=[gap],
        hypotheses=[hypothesis],
    )

    assert result.contradictions == [contradiction]
    assert result.gaps == [gap]
    assert result.hypotheses == [hypothesis]


def test_empty_analysis_result_has_zero_counts():
    result = AnalysisResult()

    assert result.contradiction_count == 0
    assert result.gap_count == 0
    assert result.hypothesis_count == 0