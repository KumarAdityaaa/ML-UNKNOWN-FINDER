from unknown_finder.parsing.models import ParsedDocument


def test_parsed_document():
    document = ParsedDocument(
        paper_id="test-001",
        title="Test Paper",
    )

    assert document.paper_id == "test-001"
    assert document.title == "Test Paper"
    assert document.sections == []
    assert document.references == []