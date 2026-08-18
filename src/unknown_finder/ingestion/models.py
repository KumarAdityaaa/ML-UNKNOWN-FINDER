from datetime import date
from pydantic import BaseModel, Field


class PaperRecord(BaseModel):
    paper_id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    abstract: str | None = None
    publication_date: date | None = None
    venue: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    pmid: str | None = None
    openalex_id: str | None = None
    source: str
    landing_page: str | None = None
    pdf_url: str | None = None