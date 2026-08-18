from unknown_finder.ingestion.provenance import PDFProvenance


def test_pdf_provenance():
    provenance = PDFProvenance.create(
        paper_id="paper-001",
        source_url="https://example.org/paper.pdf",
        local_path="data/paper.pdf",
    )

    assert provenance.paper_id == "paper-001"
    assert provenance.source_url == "https://example.org/paper.pdf"
    assert provenance.local_path == "data/paper.pdf"
    assert provenance.downloaded_at is not None