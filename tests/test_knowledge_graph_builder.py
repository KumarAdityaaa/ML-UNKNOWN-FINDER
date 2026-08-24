from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.knowledge_graph.builder import build_knowledge_graph


def test_build_knowledge_graph_from_claims_and_evidence():
    claims = [
        Claim(
            claim_id="claim-001",
            text="The proposed method improves accuracy.",
            paper_id="paper-001",
            section="Results",
        ),
    ]

    evidence = [
        Evidence(
            evidence_id="evidence-001",
            claim_id="claim-001",
            text="Accuracy improved by 5 percent.",
            paper_id="paper-001",
            evidence_type="supporting",
        ),
    ]

    graph = build_knowledge_graph(claims, evidence)

    assert graph.claims["claim-001"] == claims[0]
    assert graph.evidence["evidence-001"] == evidence[0]
    assert graph.get_evidence_for_claim("claim-001") == [evidence[0]]

def test_build_knowledge_graph_rejects_orphan_evidence():
    import pytest

    evidence = [
        Evidence(
            evidence_id="evidence-001",
            claim_id="missing-claim",
            text="Unsupported evidence.",
            paper_id="paper-001",
            evidence_type="supporting",
        ),
    ]

    with pytest.raises(ValueError, match="unknown claim"):
        build_knowledge_graph([], evidence)