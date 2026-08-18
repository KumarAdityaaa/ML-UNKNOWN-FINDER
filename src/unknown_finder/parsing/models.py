from pydantic import BaseModel, Field


class DocumentSection(BaseModel):
    heading: str
    text: str
    level: int = 1


class ParsedDocument(BaseModel):
    paper_id: str
    title: str
    abstract: str | None = None
    sections: list[DocumentSection] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)