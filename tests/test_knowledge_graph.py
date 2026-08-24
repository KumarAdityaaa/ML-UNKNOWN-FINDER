from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.knowledge_graph.models import KnowledgeGraph
from unknown_finder.extraction.concepts import Concept

def test_knowledge_graph_adds_claim_and_evidence():
    graph = KnowledgeGraph()

    claim = Claim(
        claim_id="claim-001",
        text="The proposed method improves accuracy.",
        paper_id="paper-001",
        section="Results",
    )

    evidence = Evidence(
        evidence_id="evidence-001",
        claim_id="claim-001",
        text="The method improved accuracy by 5 percent.",
        paper_id="paper-001",
        evidence_type="supporting",
    )

    graph.add_claim(claim)
    graph.add_evidence(evidence)

    assert graph.claims["claim-001"] == claim
    assert graph.evidence["evidence-001"] == evidence

def test_knowledge_graph_rejects_orphan_evidence():
    import pytest

    graph = KnowledgeGraph()

    evidence = Evidence(
        evidence_id="evidence-001",
        claim_id="missing-claim",
        text="Unsupported evidence.",
        paper_id="paper-001",
        evidence_type="supporting",
    )

    with pytest.raises(ValueError, match="unknown claim"):
        graph.add_evidence(evidence)

def test_knowledge_graph_get_evidence_for_claim():
    graph = KnowledgeGraph()

    claim = Claim(
        claim_id="claim-001",
        text="The proposed method improves accuracy.",
        paper_id="paper-001",
        section="Results",
    )

    evidence_one = Evidence(
        evidence_id="evidence-001",
        claim_id="claim-001",
        text="Accuracy improved by 5 percent.",
        paper_id="paper-001",
        evidence_type="supporting",
    )

    evidence_two = Evidence(
        evidence_id="evidence-002",
        claim_id="claim-001",
        text="The improvement was consistent across datasets.",
        paper_id="paper-001",
        evidence_type="supporting",
    )

    graph.add_claim(claim)
    graph.add_evidence(evidence_one)
    graph.add_evidence(evidence_two)

    evidence = graph.get_evidence_for_claim("claim-001")

    assert evidence == [evidence_one, evidence_two]

def test_knowledge_graph_returns_empty_for_unknown_claim():
    graph = KnowledgeGraph()

    assert graph.get_evidence_for_claim("missing-claim") == []

def test_knowledge_graph_tracks_papers_for_claims():
    graph = KnowledgeGraph()

    claim = Claim(
        claim_id="claim-001",
        text="The proposed method improves accuracy.",
        paper_id="paper-001",
        section="Results",
    )

    graph.add_claim(claim)

    assert graph.get_claims_for_paper("paper-001") == [claim]
    assert graph.get_claims_for_paper("missing-paper") == []

def test_knowledge_graph_tracks_concepts():
    graph = KnowledgeGraph()

    concept = Concept(
        term="self attention",
        frequency=3,
        sections=["Introduction", "Methods"],
        contexts=["self attention improves sequence modeling."],
        score=5.25,
    )

    graph.add_concept(concept)

    assert graph.concepts["self attention"] == concept
    assert graph.get_concepts_for_section("Introduction") == [concept]
    assert graph.get_concepts_for_section("Methods") == [concept]
    assert graph.get_concepts_for_section("Results") == []