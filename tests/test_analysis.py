from unknown_finder.parsing.analysis import analyze_document
from unknown_finder.parsing.models import (
    Citation,
    DocumentSection,
    ParsedDocument,
    Reference,
)


def test_analyze_document():
    document = ParsedDocument(
        paper_id="test-001",
        title="Test Paper",
        abstract="This is an abstract.",
        sections=[
            DocumentSection(
                heading="Introduction",
                text="Introduction text.",
            ),
            DocumentSection(
                heading="Results",
                text="Results text.",
            ),
        ],
        references=[
            Reference(
                reference_id="1",
                text="First reference.",
            ),
            Reference(
                reference_id="2",
                text="Second reference.",
            ),
        ],
        citations=[
            Citation(
                reference_id="2",
                context="Previous work [2].",
            ),
            Citation(
                reference_id="1",
                context="Earlier work [1].",
            ),
            Citation(
                reference_id="2",
                context="Further work [2].",
            ),
        ],
    )

    analysis = analyze_document(document)

    assert analysis.paper_id == "test-001"
    assert analysis.title == "Test Paper"
    assert analysis.abstract_length == len("This is an abstract.")
    assert analysis.section_count == 2
    assert analysis.reference_count == 2
    assert analysis.citation_count == 3
    assert analysis.cited_reference_ids == ["1", "2"]


def test_analyze_empty_document():
    document = ParsedDocument(
        paper_id="empty",
        title="",
    )

    analysis = analyze_document(document)

    assert analysis.paper_id == "empty"
    assert analysis.abstract_length == 0
    assert analysis.section_count == 0
    assert analysis.reference_count == 0
    assert analysis.citation_count == 0
    assert analysis.cited_reference_ids == []