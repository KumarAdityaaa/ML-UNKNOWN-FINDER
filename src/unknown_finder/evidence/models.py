from typing import Literal

from pydantic import BaseModel


class Claim(BaseModel):
    claim_id: str
    text: str
    paper_id: str
    section: str


class Evidence(BaseModel):
    evidence_id: str
    claim_id: str
    text: str
    paper_id: str
    evidence_type: Literal[
        "supporting",
        "contradicting",
        "context",
    ]