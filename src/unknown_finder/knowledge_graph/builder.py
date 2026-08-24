from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.extraction.concepts import Concept
from unknown_finder.knowledge_graph.models import KnowledgeGraph
from unknown_finder.knowledge_graph.relationships import (
    link_claims_to_concepts,
)


def build_knowledge_graph(
    claims: list[Claim],
    evidence: list[Evidence],
    concepts: list[Concept] | None = None,
) -> KnowledgeGraph:
    graph = KnowledgeGraph()

    # 1. Add claims
    for claim in claims:
        graph.add_claim(claim)

    # 2. Add evidence
    for item in evidence:
        graph.add_evidence(item)

    # 3. Add concepts
    for concept in concepts or []:
        graph.add_concept(concept)

    # 4. Create Claim -> Concept relationships
    links = link_claims_to_concepts(
        claims,
        concepts or [],
    )

    for claim_id, concept_term in links:
        graph.link_claim_to_concept(
            claim_id,
            concept_term,
        )

    for concept in concepts or []:
        graph.add_concept(concept)

    links = link_claims_to_concepts(
        claims,
        concepts or [],
    )

    for claim_id, concept_term in links:
        graph.link_claim_to_concept(
            claim_id,
            concept_term,
        )

    return graph