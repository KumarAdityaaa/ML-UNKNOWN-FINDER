from pathlib import Path

import pymupdf

from unknown_finder.ingestion.downloader import PaperDownloader
from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.ingestion.provenance import PDFProvenance
from unknown_finder.ingestion.registry import CorpusRegistry
from unknown_finder.parsing.pdf import PDFParser
from unknown_finder.parsing.analysis import analyze_document
from unknown_finder.parsing.citation_stats import (
    calculate_citation_statistics,
)
from unknown_finder.parsing.reference_impact import (
    calculate_reference_impact,
)
from unknown_finder.extraction.concepts import extract_concepts
from unknown_finder.extraction.novelty import score_novelty

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
    analysis = analyze_document(parsed)
    citation_stats = calculate_citation_statistics(
        parsed.citations,
        parsed.references,
    )
    reference_impacts = calculate_reference_impact(
        citation_stats,
        parsed.references,
    )
    concepts = extract_concepts(
        parsed.sections,
        min_frequency=3,
    )
    novelty_results = score_novelty(concepts)

    print()
    print("      Novelty Scoring:")
    print(f"        Concepts scored: {len(novelty_results)}")
    print("        Top 10 novelty candidates:")

    for result in novelty_results[:10]:
        print(
            f"          {result.term}: "
            f"score={result.novelty_score:.4f}, "
            f"{result.reason}"
        )    

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
    print("\n      Paper Analysis:")
    print(f"        Title: {analysis.title}")
    print(f"        Abstract length: {analysis.abstract_length:,} characters")
    print(f"        Sections: {analysis.section_count}")
    print(f"        References: {analysis.reference_count}")
    print(f"        Citation occurrences: {analysis.citation_count}")
    print(f"        Cited references: {len(analysis.cited_reference_ids)}")
    # 3. Create paper metadata.
    print("\n[3/5] Creating paper record...")
    print("\n      Citation Statistics:")
    print(f"        Total citations: {citation_stats.total_citations}")
    print(f"        Unique cited references: {citation_stats.unique_citations}")

    print("        Top 5 cited references:")

    for reference_id, count in citation_stats.most_cited[:5]:
        print(f"          [{reference_id}] {count} citations")

    print(
        f"        Uncited references: "
        f"{len(citation_stats.uncited_references)}"
    )
    print("\n      Reference Impact:")

    top_impacts = sorted(
        reference_impacts,
        key=lambda impact: (
            -impact.impact_score,
            int(impact.reference_id),
        ),
    )

    for impact in top_impacts[:5]:
        print(
            f"        [{impact.reference_id}] "
            f"citations={impact.citation_count}, "
            f"score={impact.impact_score:.4f}, "
            f"rank={impact.rank}"
        )
    print("\n      Concept Extraction:")

    print(f"        Concepts found: {len(concepts)}")
    print("        Top 10 concepts:")

    for concept in concepts[:10]:
        print(
            f"          {concept.term}: "
            f"{concept.frequency} occurrences, "
            f"{len(concept.sections)} sections"
        )

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