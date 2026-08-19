from unknown_finder.parsing.citation_validation import validate_citations
from unknown_finder.parsing.models import Citation, Reference


def test_validate_citations():
    references = [
        Reference(reference_id="1", text="First reference"),
        Reference(reference_id="2", text="Second reference"),
    ]

    citations = [
        Citation(reference_id="1", context="Previous work [1]."),
        Citation(reference_id="2", context="Later work [2]."),
        Citation(reference_id="9", context="Unknown work [9]."),
    ]

    valid = validate_citations(citations, references)

    assert len(valid) == 2
    assert [citation.reference_id for citation in valid] == ["1", "2"]


def test_validate_citations_empty():
    references = [
        Reference(reference_id="1", text="First reference"),
    ]

    citations = [
        Citation(reference_id="9", context="Unknown [9]."),
    ]

    assert validate_citations(citations, references) == []