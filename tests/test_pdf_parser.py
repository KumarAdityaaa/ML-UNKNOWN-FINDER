import fitz

from unknown_finder.parsing.pdf import PDFParser


def test_pdf_parser(tmp_path):
    pdf_path = tmp_path / "test_document.pdf"

    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "AI Unknown Finder Test Document")
    document.save(pdf_path)
    document.close()

    parsed = PDFParser().parse(pdf_path)

    assert parsed.paper_id == str(pdf_path)
    assert "AI Unknown Finder Test Document" in parsed.sections[0].text