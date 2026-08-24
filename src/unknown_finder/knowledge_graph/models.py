from unknown_finder.evidence.models import Claim, Evidence
from unknown_finder.extraction.concepts import Concept

class KnowledgeGraph:
    def __init__(self):
        self.claims: dict[str, Claim] = {}
        self.evidence: dict[str, Evidence] = {}
        self.concepts: dict[str, Concept] = {}
        self.claim_concepts: dict[str, list[str]] = {}

    def add_claim(self, claim: Claim) -> None:
        self.claims[claim.claim_id] = claim

    def add_evidence(self, evidence: Evidence) -> None:
        if evidence.claim_id not in self.claims:
            raise ValueError(
                f"Evidence {evidence.evidence_id!r} references "
                f"unknown claim {evidence.claim_id!r}"
            )

        self.evidence[evidence.evidence_id] = evidence

    def get_evidence_for_claim(
        self,
        claim_id: str,
    ) -> list[Evidence]:
        return [
            evidence
            for evidence in self.evidence.values()
            if evidence.claim_id == claim_id
        ]

    def get_claims_for_paper(
        self,
        paper_id: str,
    ) -> list[Claim]:
        return [
            claim
            for claim in self.claims.values()
            if claim.paper_id == paper_id
        ]

    def add_concept(self, concept: Concept) -> None:
        self.concepts[concept.term] = concept

    def get_concepts_for_section(
        self,
        section: str,
    ) -> list[Concept]:
        return [
            concept
            for concept in self.concepts.values()
            if section in concept.sections
        ]

    def link_claim_to_concept(
        self,
        claim_id: str,
        concept_term: str,
    ) -> None:
        if claim_id not in self.claims:
            raise ValueError(
                f"Unknown claim {claim_id!r}"
            )

        if concept_term not in self.concepts:
            raise ValueError(
                f"Unknown concept {concept_term!r}"
            )

        self.claim_concepts.setdefault(
            claim_id,
            [],
        )

        if concept_term not in self.claim_concepts[claim_id]:
            self.claim_concepts[claim_id].append(concept_term)

    def get_concepts_for_claim(
        self,
        claim_id: str,
    ) -> list[Concept]:
        return [
            self.concepts[term]
            for term in self.claim_concepts.get(claim_id, [])
        ]

    def get_claim_trace(
        self,
        claim_id: str,
    ) -> dict:
        claim = self.claims.get(claim_id)

        if claim is None:
            return {
                "claim": None,
                "concepts": [],
                "evidence": [],
            }

        return {
            "claim": claim,
            "concepts": self.get_concepts_for_claim(claim_id),
            "evidence": self.get_evidence_for_claim(claim_id),
        }