from unknown_finder.ingestion.evaluation import (
    IngestionEvaluationCase,
    evaluate_sources,
)


def test_evaluate_sources():
    cases = [
        IngestionEvaluationCase(
            query="machine learning",
            expected_sources={"openalex", "arxiv"},
        ),
        IngestionEvaluationCase(
            query="computer vision",
            expected_sources={"openalex"},
        ),
    ]

    actual_sources = {
        "machine learning": {"openalex", "arxiv"},
        "computer vision": {"openalex"},
    }

    score = evaluate_sources(cases, actual_sources)

    assert score == 1.0


def test_evaluate_sources_partial_score():
    cases = [
        IngestionEvaluationCase(
            query="machine learning",
            expected_sources={"openalex", "arxiv"},
        )
    ]

    actual_sources = {
        "machine learning": {"openalex"},
    }

    score = evaluate_sources(cases, actual_sources)

    assert score == 0.5