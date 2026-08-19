from pydantic import BaseModel, Field


class DocumentSection(BaseModel):
    heading: str
    text: str
    level: int = 1


class Reference(BaseModel):
    reference_id: str
    text: str


class ParsedDocument(BaseModel):
    paper_id: str
    title: str
    abstract: str | None = None
    sections: list[DocumentSection] = Field(default_factory=list)
    references: list[Reference] = Field(default_factory=list)