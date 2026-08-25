from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.knowledge_graph.models import KnowledgeGraph
from unknown_finder.extraction.concepts import Concept
from unknown_finder.knowledge_graph.builder import build_knowledge_graph
from unknown_finder.contradiction.models import Contradiction
import pytest

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

def test_knowledge_graph_tracks_claim_concept_relationships():
    graph = KnowledgeGraph()

    claim = Claim(
        claim_id="claim-001",
        text="Self attention improves sequence modeling.",
        paper_id="paper-001",
        section="Results",
    )

    concept = Concept(
        term="self attention",
        frequency=3,
        sections=["Results"],
        contexts=["Self attention improves sequence modeling."],
        score=5.2,
    )

    graph.add_claim(claim)
    graph.add_concept(concept)
    graph.link_claim_to_concept(claim.claim_id, concept.term)

    assert graph.get_concepts_for_claim("claim-001") == [concept]

def test_knowledge_graph_returns_claim_trace():
    graph = KnowledgeGraph()

    claim = Claim(
        claim_id="claim-001",
        text="Self attention improves sequence modeling.",
        paper_id="paper-001",
        section="Results",
    )

    concept = Concept(
        term="self attention",
        frequency=3,
        sections=["Results"],
        contexts=["Self attention improves sequence modeling."],
        score=5.2,
    )

    evidence = Evidence(
        evidence_id="evidence-001",
        claim_id="claim-001",
        text="Accuracy improved by 5 percent.",
        paper_id="paper-001",
        evidence_type="supporting",
    )

    graph.add_claim(claim)
    graph.add_concept(concept)
    graph.add_evidence(evidence)
    graph.link_claim_to_concept(
        "claim-001",
        "self attention",
    )

    trace = graph.get_claim_trace("claim-001")

    assert trace["claim"] == claim
    assert trace["concepts"] == [concept]
    assert trace["evidence"] == [evidence]

def test_knowledge_graph_returns_empty_trace_for_unknown_claim():
    graph = KnowledgeGraph()

    trace = graph.get_claim_trace("missing-claim")

    assert trace == {
        "claim": None,
        "concepts": [],
        "evidence": [],
    }

def test_build_knowledge_graph_provides_claim_trace():
    claims = [
        Claim(
            claim_id="claim-001",
            text="Self attention improves sequence modeling.",
            paper_id="paper-001",
            section="Results",
        ),
    ]

    concepts = [
        Concept(
            term="self attention",
            frequency=3,
            sections=["Results"],
            contexts=["Self attention improves sequence modeling."],
            score=5.2,
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

    graph = build_knowledge_graph(
        claims=claims,
        evidence=evidence,
        concepts=concepts,
    )

    trace = graph.get_claim_trace("claim-001")

    assert trace["claim"] == claims[0]
    assert trace["concepts"] == [concepts[0]]
    assert trace["evidence"] == [evidence[0]]

def test_knowledge_graph_tracks_contradictions():
    graph = KnowledgeGraph()

    claim_a = Claim(
        claim_id="claim-001",
        text="The proposed method improves accuracy.",
        paper_id="paper-001",
        section="Results",
    )

    claim_b = Claim(
        claim_id="claim-002",
        text="The proposed method does not improve accuracy.",
        paper_id="paper-002",
        section="Results",
    )

    graph.add_claim(claim_a)
    graph.add_claim(claim_b)

    contradiction = Contradiction(
        claim_a="claim-001",
        claim_b="claim-002",
        paper_a="paper-001",
        paper_b="paper-002",
    )

    graph.add_contradiction(contradiction)

    assert graph.get_contradictions_for_claim("claim-001") == [
        contradiction
    ]
    assert graph.get_contradictions_for_claim("claim-002") == [
        contradiction
    ]

def test_knowledge_graph_rejects_contradiction_with_unknown_claim():

    graph = KnowledgeGraph()

    claim = Claim(
        claim_id="claim-001",
        text="The proposed method improves accuracy.",
        paper_id="paper-001",
        section="Results",
    )

    graph.add_claim(claim)

    contradiction = Contradiction(
        claim_a="claim-001",
        claim_b="missing-claim",
        paper_a="paper-001",
        paper_b="paper-002",
    )

    with pytest.raises(ValueError, match="Unknown claim"):
        graph.add_contradiction(contradiction)

def test_knowledge_graph_does_not_duplicate_contradictions():
    graph = KnowledgeGraph()

    claim_a = Claim(
        claim_id="claim-001",
        text="The proposed method improves accuracy.",
        paper_id="paper-001",
        section="Results",
    )

    claim_b = Claim(
        claim_id="claim-002",
        text="The proposed method does not improve accuracy.",
        paper_id="paper-002",
        section="Results",
    )

    graph.add_claim(claim_a)
    graph.add_claim(claim_b)

    contradiction = Contradiction(
        claim_a="claim-001",
        claim_b="claim-002",
        paper_a="paper-001",
        paper_b="paper-002",
    )

    graph.add_contradiction(contradiction)
    graph.add_contradiction(contradiction)

    assert graph.get_contradictions_for_claim("claim-001") == [
        contradiction
    ]
    assert graph.get_contradictions_for_claim("claim-002") == [
        contradiction
    ]

def test_knowledge_graph_returns_empty_for_unknown_contradiction_claim():
    graph = KnowledgeGraph()

    assert graph.get_contradictions_for_claim("missing-claim") == []