from unknown_finder.parsing.citations import extract_citations


def test_extract_citations():
    text = """
Attention mechanisms have been widely studied [1].

Several approaches have been proposed [2, 3].

The Transformer builds on these ideas [1, 4].
"""

    citations = extract_citations(text)

    assert len(citations) == 5

    assert citations[0].reference_id == "1"
    assert citations[1].reference_id == "2"
    assert citations[2].reference_id == "3"
    assert citations[3].reference_id == "1"
    assert citations[4].reference_id == "4"

    assert "Attention mechanisms" in citations[0].context


def test_extract_citations_empty():
    citations = extract_citations(
        "This text contains no citations."
    )

    assert citations == []

def test_citation_ids_are_preserved():
    text = """
    Previous work [1] established the method.
    Later work [2, 3] improved it.
    """

    citations = extract_citations(text)

    assert [citation.reference_id for citation in citations] == [
        "1",
        "2",
        "3",
    ]

    assert all(citation.context for citation in citations)

def test_citations_can_link_to_references():
    references = {
        "1": "First reference",
        "2": "Second reference",
        "3": "Third reference",
    }

    text = """
    Previous work [1] established the method.
    Later work [2, 3] improved it.
    """

    citations = extract_citations(text)

    citation_ids = {
        citation.reference_id
        for citation in citations
    }

    assert citation_ids.issubset(references.keys())