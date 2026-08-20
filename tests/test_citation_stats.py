from unknown_finder.parsing.citation_stats import (
    calculate_citation_statistics,
)
from unknown_finder.parsing.models import Citation, Reference


def test_calculate_citation_statistics():
    references = [
        Reference(reference_id="1", text="First"),
        Reference(reference_id="2", text="Second"),
        Reference(reference_id="3", text="Third"),
        Reference(reference_id="4", text="Fourth"),
    ]

    citations = [
        Citation(reference_id="1", context="A [1]."),
        Citation(reference_id="2", context="B [2]."),
        Citation(reference_id="1", context="C [1]."),
        Citation(reference_id="1", context="D [1]."),
        Citation(reference_id="3", context="E [3]."),
    ]

    stats = calculate_citation_statistics(
        citations,
        references,
    )

    assert stats.total_citations == 5
    assert stats.unique_citations == 3

    assert stats.citation_frequency == {
        "1": 3,
        "2": 1,
        "3": 1,
    }

    assert stats.most_cited == [
        ("1", 3),
        ("2", 1),
        ("3", 1),
    ]

    assert stats.uncited_references == ["4"]


def test_empty_citation_statistics():
    references = [
        Reference(reference_id="1", text="First"),
        Reference(reference_id="2", text="Second"),
    ]

    stats = calculate_citation_statistics(
        [],
        references,
    )

    assert stats.total_citations == 0
    assert stats.unique_citations == 0
    assert stats.citation_frequency == {}
    assert stats.most_cited == []
    assert stats.uncited_references == ["1", "2"]