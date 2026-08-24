from unknown_finder.evidence.models import Claim
from unknown_finder.extraction.concepts import Concept
from unknown_finder.knowledge_graph.relationships import link_claims_to_concepts


def test_link_claim_to_concept():
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

    links = link_claims_to_concepts(
        [claim],
        [concept],
    )

    assert links == [("claim-001", "self attention")]

def test_link_claims_to_concepts_ignores_unmentioned_concepts():
    claim = Claim(
        claim_id="claim-001",
        text="Self attention improves sequence modeling.",
        paper_id="paper-001",
        section="Results",
    )

    concepts = [
        Concept(
            term="self attention",
            frequency=3,
            sections=["Results"],
            contexts=["Self attention improves sequence modeling."],
            score=5.2,
        ),
        Concept(
            term="convolutional network",
            frequency=2,
            sections=["Methods"],
            contexts=["Convolutional networks were used elsewhere."],
            score=3.1,
        ),
    ]

    links = link_claims_to_concepts([claim], concepts)

    assert links == [("claim-001", "self attention")]