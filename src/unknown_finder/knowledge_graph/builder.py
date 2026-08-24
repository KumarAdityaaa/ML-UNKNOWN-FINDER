from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.knowledge_graph.models import KnowledgeGraph


def build_knowledge_graph(
    claims: list[Claim],
    evidence: list[Evidence],
) -> KnowledgeGraph:
    graph = KnowledgeGraph()

    for claim in claims:
        graph.add_claim(claim)

    for item in evidence:
        graph.add_evidence(item)

    return graph