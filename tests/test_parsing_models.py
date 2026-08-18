from unknown_finder.parsing.models import DocumentSection, ParsedDocument


def test_parsed_document():
    document = ParsedDocument(
        paper_id="test-001",
        title="Test Paper",
        sections=[
            DocumentSection(
                heading="Introduction",
                text="This is an introduction.",
                level=1,
            )
        ],
    )

    assert document.paper_id == "test-001"
    assert document.title == "Test Paper"
    assert len(document.sections) == 1
    assert document.sections[0].heading == "Introduction"
    assert document.sections[0].text == "This is an introduction."
    assert document.sections[0].level == 1
    assert document.references == []