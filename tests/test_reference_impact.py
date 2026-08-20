from unknown_finder.parsing.citation_stats import CitationStatistics
from unknown_finder.parsing.models import Reference
from unknown_finder.parsing.reference_impact import (
    calculate_reference_impact,
)


def test_calculate_reference_impact():
    statistics = CitationStatistics(
        total_citations=6,
        unique_citations=3,
        citation_frequency={
            "1": 6,
            "2": 3,
            "3": 1,
        },
        most_cited=[
            ("1", 6),
            ("2", 3),
            ("3", 1),
        ],
        uncited_references=["4"],
    )

    references = [
        Reference(reference_id="1", text="First"),
        Reference(reference_id="2", text="Second"),
        Reference(reference_id="3", text="Third"),
        Reference(reference_id="4", text="Fourth"),
    ]

    impacts = calculate_reference_impact(
        statistics,
        references,
    )

    assert impacts[0].reference_id == "1"
    assert impacts[0].citation_count == 6
    assert impacts[0].impact_score == 1.0
    assert impacts[0].rank == 1

    assert impacts[1].reference_id == "2"
    assert impacts[1].citation_count == 3
    assert impacts[1].impact_score == 0.5
    assert impacts[1].rank == 2

    assert impacts[2].reference_id == "3"
    assert impacts[2].citation_count == 1
    assert impacts[2].impact_score == 0.1667
    assert impacts[2].rank == 3

    assert impacts[3].reference_id == "4"
    assert impacts[3].citation_count == 0
    assert impacts[3].impact_score == 0.0
    assert impacts[3].rank == 0


def test_reference_impact_without_citations():
    statistics = CitationStatistics(
        total_citations=0,
        unique_citations=0,
        citation_frequency={},
        most_cited=[],
        uncited_references=["1", "2"],
    )

    references = [
        Reference(reference_id="1", text="First"),
        Reference(reference_id="2", text="Second"),
    ]

    impacts = calculate_reference_impact(
        statistics,
        references,
    )

    assert len(impacts) == 2

    for impact in impacts:
        assert impact.citation_count == 0
        assert impact.impact_score == 0.0
        assert impact.rank == 0