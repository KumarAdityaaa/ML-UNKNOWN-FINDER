from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):
    paper_id: str
    title: str
    abstract: str | None = None
    sections: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)