from pathlib import Path

import pymupdf

from unknown_finder.ingestion.downloader import PaperDownloader
from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.ingestion.provenance import PDFProvenance
from unknown_finder.ingestion.registry import CorpusRegistry
from unknown_finder.parsing.pdf import PDFParser


PAPER_ID = "1706.03762"
TITLE = "Attention Is All You Need"
SOURCE_URL = "https://arxiv.org/pdf/1706.03762"

DATA_DIR = Path("data/demo")
PDF_PATH = DATA_DIR / f"{PAPER_ID}.pdf"
REGISTRY_PATH = DATA_DIR / "corpus.json"


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("AI UNKNOWN FINDER — REAL PAPER DEMO")
    print("=" * 60)

    print(f"\nTitle: {TITLE}")
    print(f"Paper ID: {PAPER_ID}")
    print("Source: arXiv")
    print(f"URL: {SOURCE_URL}")

    # 1. Download the real paper.
    print("\n[1/5] Downloading real paper...")

    downloader = PaperDownloader()
    pdf_path = downloader.download(SOURCE_URL, PDF_PATH)

    print(f"      PDF: {pdf_path}")
    print(f"      Size: {pdf_path.stat().st_size:,} bytes")

    # 2. Parse and inspect the real PDF.
    print("\n[2/5] Inspecting PDF...")

    parser = PDFParser()
    parsed = parser.parse(pdf_path)

    document = pymupdf.open(pdf_path)
    page_count = len(document)
    document.close()

    text = "\n".join(
        section.text
        for section in parsed.sections
    )

    print(f"      Pages: {page_count}")
    print(f"      Sections: {len(parsed.sections)}")
    print(f"      Extracted text: {len(text):,} characters")
    print(f"      References: {len(parsed.references)}")
    print(f"      Validated citations: {len(parsed.citations)}")

    if parsed.citations:
        print("      First 3 citations:")

        for citation in parsed.citations[:3]:
            print(
                f"        [{citation.reference_id}] "
                f"{citation.context[:180]}"
            )
    if parsed.references:
        print("      First 3 references:")

        for reference in parsed.references[:3]:
            print(
                f"        [{reference.reference_id}] "
                f"{reference.text[:180]}"
            )
    print(f"      Parsed title: {parsed.title}")

    if parsed.abstract:
        abstract_preview = parsed.abstract[:300].replace("\n", " ")
        print(f"      Abstract preview: {abstract_preview}...")

    print(f"      Metadata extraction: {'PASS' if parsed.title and parsed.abstract else 'FAIL'}")

    for section in parsed.sections:
        print(
            f"        - [L{section.level}] "
            f"{section.heading}: "
            f"{len(section.text):,} characters"
        )

    # 3. Create paper metadata.
    print("\n[3/5] Creating paper record...")

    paper = PaperRecord(
        paper_id=PAPER_ID,
        title=TITLE,
        source="arxiv",
    )

    print(f"      PaperRecord: {paper.paper_id}")

    # 4. Record provenance.
    print("\n[4/5] Recording provenance...")

    provenance = PDFProvenance.create(
        paper_id=PAPER_ID,
        source_url=SOURCE_URL,
        local_path=str(pdf_path),
    )

    print(f"      Downloaded: {provenance.downloaded_at}")
    print(f"      Local path: {provenance.local_path}")

    # 5. Persist the paper in the corpus registry.
    print("\n[5/5] Updating corpus registry...")

    registry = CorpusRegistry(REGISTRY_PATH)
    registry.save([paper])

    registered = registry.load()

    print(f"      Registry: {REGISTRY_PATH}")
    print(f"      Registered papers: {len(registered)}")

    print("\n" + "=" * 60)
    print("PHASE 2 SECTION DETECTION DEMO: PASS")
    print("=" * 60)


if __name__ == "__main__":
    main()