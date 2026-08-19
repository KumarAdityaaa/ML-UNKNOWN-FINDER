import pymupdf

from .metadata import extract_metadata
from .models import ParsedDocument
from .references import extract_references
from .sections import detect_sections
from .citations import extract_citations


class PDFParser:
    def parse(self, path: str) -> ParsedDocument:
        document = pymupdf.open(path)

        text = "\n".join(
            page.get_text()
            for page in document
        )

        document.close()

        metadata = extract_metadata(text)
        references = extract_references(text)
        citations = extract_citations(text)

        return ParsedDocument(
            paper_id=str(path),
            title=metadata["title"],
            abstract=metadata["abstract"] or None,
            sections=detect_sections(text),
            references=references,
            citations=citations,
        )