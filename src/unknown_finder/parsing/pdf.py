import pymupdf
from .models import ParsedDocument
from .sections import detect_sections


class PDFParser:
    def parse(self, path: str) -> ParsedDocument:
        document = pymupdf.open(path)

        text = "\n".join(page.get_text() for page in document)

        document.close()

        return ParsedDocument(
            paper_id=str(path),
            title="",
            sections=detect_sections(text),
        )