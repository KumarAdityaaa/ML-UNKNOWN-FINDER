from unknown_finder.extraction.novelty import NoveltyResult
from unknown_finder.ingestion.models import PaperRecord
from unknown_finder.novelty.ranking import rank_unknowns


def test_rank_unknowns_orders_by_novelty_score():
    papers = [
        PaperRecord(
            paper_id="paper-001",
            title="Paper One",
            source="test",
            novelty_results=[
                NoveltyResult(
                    term="common method",
                    novelty_score=0.30,
                    reason="relatively common technical concept",
                ),
                NoveltyResult(
                    term="adaptive attention",
                    novelty_score=0.90,
                    reason="rare and specific technical concept",
                ),
            ],
        ),
        PaperRecord(
            paper_id="paper-002",
            title="Paper Two",
            source="test",
            novelty_results=[
                NoveltyResult(
                    term="sparse routing",
                    novelty_score=0.70,
                    reason="rare and specific technical concept",
                ),
            ],
        ),
    ]

    ranked = rank_unknowns(papers)

    assert [result.term for result in ranked] == [
        "adaptive attention",
        "sparse routing",
        "common method",
    ]
def test_rank_unknowns_deduplicates_terms():
    papers = [
        PaperRecord(
            paper_id="paper-001",
            title="Paper One",
            source="test",
            novelty_results=[
                NoveltyResult(
                    term="adaptive attention",
                    novelty_score=0.70,
                    reason="rare and specific technical concept",
                ),
            ],
        ),
        PaperRecord(
            paper_id="paper-002",
            title="Paper Two",
            source="test",
            novelty_results=[
                NoveltyResult(
                    term="adaptive attention",
                    novelty_score=0.90,
                    reason="rare and specific technical concept",
                ),
                NoveltyResult(
                    term="sparse routing",
                    novelty_score=0.80,
                    reason="rare and specific technical concept",
                ),
            ],
        ),
    ]

    ranked = rank_unknowns(papers)

    assert [result.term for result in ranked] == [
        "adaptive attention",
        "sparse routing",
    ]
    assert ranked[0].novelty_score == 0.90
    assert ranked[0].paper_id == "paper-002"
    assert ranked[0].paper_title == "Paper Two"

def test_rank_unknowns_returns_empty_list_for_empty_corpus():
    assert rank_unknowns([]) == []

def test_rank_unknowns_keeps_source_paper():
    paper = PaperRecord(
        paper_id="paper-123",
        title="Attention Research",
        source="test",
        novelty_results=[
            NoveltyResult(
                term="adaptive attention",
                novelty_score=0.91,
                reason="rare and specific technical concept",
            ),
        ],
    )

    ranked = rank_unknowns([paper])

    assert ranked[0].term == "adaptive attention"
    assert ranked[0].paper_id == "paper-123"
    assert ranked[0].paper_title == "Attention Research"

def test_rank_unknowns_tracks_multiple_source_papers():
    papers = [
        PaperRecord(
            paper_id="paper-001",
            title="Paper One",
            source="test",
            novelty_results=[
                NoveltyResult(
                    term="adaptive attention",
                    novelty_score=0.80,
                    reason="rare and specific technical concept",
                ),
            ],
        ),
        PaperRecord(
            paper_id="paper-002",
            title="Paper Two",
            source="test",
            novelty_results=[
                NoveltyResult(
                    term="adaptive attention",
                    novelty_score=0.90,
                    reason="rare and specific technical concept",
                ),
            ],
        ),
    ]

    ranked = rank_unknowns(papers)

    assert ranked[0].term == "adaptive attention"
    assert ranked[0].novelty_score == 0.90
    assert ranked[0].paper_id == "paper-002"
    assert ranked[0].source_paper_ids == [
    "paper-001",
    "paper-002",
]