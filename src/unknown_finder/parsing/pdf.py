import fitz

from .models import ParsedDocument


class PDFParser:
    def parse(self, path: str) -> ParsedDocument:
        document = fitz.open(path)

        text = "\n".join(page.get_text() for page in document)

        document.close()

        return ParsedDocument(
            paper_id=str(path),
            title="",
            sections=[text],
        )