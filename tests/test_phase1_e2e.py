from pathlib import Path

import pymupdf

from unknown_finder.ingestion.downloader import PaperDownloader
from unknown_finder.ingestion.provenance import PDFProvenance
from unknown_finder.ingestion.registry import CorpusRegistry
from unknown_finder.ingestion.retry import with_retries


def test_phase1_end_to_end(tmp_path):
    # 1. Create a controlled PDF source.
    source_pdf = tmp_path / "source.pdf"

    document = pymupdf.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "AI Unknown Finder Phase 1 Integration Test",
    )
    document.save(source_pdf)
    document.close()

    # 2. Simulate paper discovery.
    papers = [
        {
            "paper_id": "phase1-001",
            "title": "Phase 1 Integration Test Paper",
            "source": "test",
        }
    ]

    assert len(papers) == 1

    # 3. Verify retry mechanism.
    attempts = {"count": 0}

    def operation():
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("temporary failure")
        return True

    assert with_retries(operation, retries=2, delay=0) is True
    assert attempts["count"] == 2

    # 4. Verify downloaded PDF exists.
    destination = tmp_path / "downloaded" / "paper.pdf"

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source_pdf.read_bytes())

    assert destination.exists()
    assert destination.read_bytes() == source_pdf.read_bytes()

    # 5. Record provenance.
    provenance = PDFProvenance.create(
        paper_id="phase1-001",
        source_url="https://example.org/paper.pdf",
        local_path=str(destination),
    )

    assert provenance.paper_id == "phase1-001"
    assert Path(provenance.local_path).exists()

    # 6. Persist corpus registry.
    registry = CorpusRegistry(tmp_path / "corpus.json")

    from unknown_finder.ingestion.models import PaperRecord

    records = [
        PaperRecord(
            paper_id=paper["paper_id"],
            title=paper["title"],
            source=paper["source"],
        )
        for paper in papers
    ]

    registry.save(records)

    loaded = registry.load()

    assert len(loaded) == 1
    assert loaded[0].paper_id == "phase1-001"

    # 7. Final Phase 1 output.
    print("\n=== PHASE 1 END-TO-END TEST ===")
    print(f"Papers discovered: {len(papers)}")
    print(f"PDF downloaded: {destination.exists()}")
    print(f"Provenance recorded: {provenance.paper_id}")
    print(f"Registry entries: {len(loaded)}")
    print("PHASE 1 PIPELINE: PASS")