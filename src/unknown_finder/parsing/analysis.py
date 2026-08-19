from dataclasses import dataclass

from .models import ParsedDocument


@dataclass
class PaperAnalysis:
    paper_id: str
    title: str
    abstract_length: int
    section_count: int
    reference_count: int
    citation_count: int
    cited_reference_ids: list[str]


def analyze_document(document: ParsedDocument) -> PaperAnalysis:
    cited_reference_ids = sorted(
        {
            citation.reference_id
            for citation in document.citations
        },
        key=int,
    )

    return PaperAnalysis(
        paper_id=document.paper_id,
        title=document.title,
        abstract_length=len(document.abstract or ""),
        section_count=len(document.sections),
        reference_count=len(document.references),
        citation_count=len(document.citations),
        cited_reference_ids=cited_reference_ids,
    )