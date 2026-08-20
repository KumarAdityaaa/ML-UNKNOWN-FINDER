from unknown_finder.extraction.concepts import Concept
from unknown_finder.extraction.novelty import (
    NoveltyResult,
    score_novelty,
)


def make_concept(
    term: str,
    frequency: int,
    sections: list[str],
    score: float,
) -> Concept:
    return Concept(
        term=term,
        frequency=frequency,
        sections=sections,
        contexts=[],
        score=score,
    )


def test_score_novelty_returns_results():
    concepts = [
        make_concept(
            "attention",
            20,
            ["Introduction", "Methods", "Results"],
            35.0,
        ),
        make_concept(
            "rare mechanism",
            2,
            ["Methods"],
            3.0,
        ),
    ]

    results = score_novelty(concepts)

    assert len(results) == 2
    assert all(
        isinstance(result, NoveltyResult)
        for result in results
    )


def test_rare_localized_technical_concept_scores_higher():
    concepts = [
        make_concept(
            "common model",
            20,
            ["Introduction", "Methods", "Results"],
            35.0,
        ),
        make_concept(
            "rare mechanism",
            2,
            ["Methods"],
            3.0,
        ),
    ]

    results = score_novelty(concepts)

    assert results[0].term == "rare mechanism"
    assert (
        results[0].novelty_score
        > results[1].novelty_score
    )


def test_novelty_score_is_bounded():
    concepts = [
        make_concept(
            "attention",
            100,
            ["Introduction"] * 20,
            500.0,
        ),
        make_concept(
            "rare mechanism",
            1,
            ["Methods"],
            0.1,
        ),
    ]

    results = score_novelty(concepts)

    assert all(
        0.0 <= result.novelty_score <= 1.0
        for result in results
    )


def test_reason_is_present():
    concepts = [
        make_concept(
            "rare mechanism",
            2,
            ["Methods"],
            3.0,
        ),
    ]

    results = score_novelty(concepts)

    assert results[0].reason
    assert "rare" in results[0].reason


def test_results_are_deterministically_sorted():
    concepts = [
        make_concept(
            "zeta mechanism",
            2,
            ["Methods"],
            3.0,
        ),
        make_concept(
            "alpha mechanism",
            2,
            ["Methods"],
            3.0,
        ),
    ]

    results = score_novelty(concepts)

    assert [result.term for result in results] == [
        "alpha mechanism",
        "zeta mechanism",
    ]


def test_person_name_is_penalized():
    concepts = [
        make_concept(
            "geoffrey",
            1,
            ["References"],
            0.5,
        ),
        make_concept(
            "adaptive attention",
            1,
            ["Methods"],
            0.5,
        ),
    ]

    results = score_novelty(concepts)

    adaptive = next(
        result
        for result in results
        if result.term == "adaptive attention"
    )

    geoffrey = next(
        result
        for result in results
        if result.term == "geoffrey"
    )

    assert adaptive.novelty_score > geoffrey.novelty_score
    assert "name" in geoffrey.reason


def test_generic_term_is_penalized():
    concepts = [
        make_concept(
            "method",
            1,
            ["Methods"],
            0.5,
        ),
        make_concept(
            "cross attention",
            1,
            ["Methods"],
            0.5,
        ),
    ]

    results = score_novelty(concepts)

    method = next(
        result
        for result in results
        if result.term == "method"
    )

    cross_attention = next(
        result
        for result in results
        if result.term == "cross attention"
    )

    assert (
        cross_attention.novelty_score
        > method.novelty_score
    )
    assert "generic" in method.reason


def test_person_name_phrase_is_penalized():
    concepts = [
        make_concept(
            "oriol vinyals",
            1,
            ["Introduction"],
            0.5,
        ),
        make_concept(
            "scaled attention",
            1,
            ["Methods"],
            0.5,
        ),
    ]

    results = score_novelty(concepts)

    name_result = next(
        result
        for result in results
        if result.term == "oriol vinyals"
    )

    technical_result = next(
        result
        for result in results
        if result.term == "scaled attention"
    )

    assert (
        technical_result.novelty_score
        > name_result.novelty_score
    )
    assert "name" in name_result.reason


def test_phrase_ending_in_and_is_penalized():
    concepts = [
        make_concept(
            "modeling and",
            1,
            ["Introduction"],
            0.5,
        ),
        make_concept(
            "sequence learning",
            1,
            ["Methods"],
            0.5,
        ),
    ]

    results = score_novelty(concepts)

    artifact = next(
        result
        for result in results
        if result.term == "modeling and"
    )

    technical = next(
        result
        for result in results
        if result.term == "sequence learning"
    )

    assert (
        technical.novelty_score
        > artifact.novelty_score
    )
    assert "artifact" in artifact.reason


def test_metadata_artifacts_are_not_novelty_candidates():
    concepts = [
        make_concept(
            "ilya sutskever",
            1,
            ["References"],
            1.0,
        ),
        make_concept(
            "pages acl",
            1,
            ["References"],
            1.0,
        ),
        make_concept(
            "additive attention",
            1,
            ["Introduction"],
            1.0,
        ),
    ]

    candidates = score_novelty(concepts)

    terms = {candidate.term for candidate in candidates}

    assert "ilya sutskever" not in terms
    assert "pages acl" not in terms
    assert "additive attention" in terms


def test_metadata_word_is_filtered_regardless_of_section():
    concepts = [
        make_concept(
            "pages acl",
            1,
            ["Introduction"],
            1.0,
        ),
        make_concept(
            "long-range dependencies",
            1,
            ["Methods"],
            1.0,
        ),
    ]

    candidates = score_novelty(concepts)

    terms = {candidate.term for candidate in candidates}

    assert "pages acl" not in terms
    assert "long-range dependencies" in terms


def test_technical_two_word_concept_is_allowed_in_body():
    concepts = [
        make_concept(
            "adaptive attention",
            1,
            ["Introduction"],
            0.5,
        ),
    ]

    candidates = score_novelty(concepts)

    terms = {candidate.term for candidate in candidates}

    assert "adaptive attention" in terms

def test_pdf_fragment_is_not_novelty_candidate():
    concepts = [
        make_concept(
            "corr abs",
            1,
            ["References"],
            1.0,
        ),
        make_concept(
            "additive attention",
            1,
            ["Introduction"],
            1.0,
        ),
    ]

    candidates = score_novelty(concepts)

    terms = {candidate.term for candidate in candidates}

    assert "corr abs" not in terms
    assert "additive attention" in terms


def test_sentence_fragment_is_not_novelty_candidate():
    concepts = [
        make_concept(
            "are missing opinion",
            1,
            ["Introduction"],
            1.0,
        ),
        make_concept(
            "long-range dependencies",
            1,
            ["Methods"],
            1.0,
        ),
    ]

    candidates = score_novelty(concepts)

    terms = {candidate.term for candidate in candidates}

    assert "are missing opinion" not in terms
    assert "long-range dependencies" in terms