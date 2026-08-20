from unknown_finder.extraction.concepts import extract_concepts
from unknown_finder.parsing.models import DocumentSection


def test_extract_concepts():
    sections = [
        DocumentSection(
            heading="Introduction",
            text=(
                "Transformer models use attention mechanisms. "
                "Attention mechanisms improve sequence modeling."
            ),
        ),
        DocumentSection(
            heading="Methods",
            text=(
                "The transformer architecture uses attention "
                "for sequence modeling."
            ),
        ),
    ]

    concepts = extract_concepts(
        sections,
        min_frequency=2,
    )

    terms = {concept.term for concept in concepts}

    assert "attention" in terms
    assert "transformer" in terms
    assert "sequence" in terms


def test_concept_frequency():
    sections = [
        DocumentSection(
            heading="Introduction",
            text="Attention attention attention.",
        ),
    ]

    concepts = extract_concepts(
        sections,
        min_frequency=2,
    )

    attention = next(
        concept
        for concept in concepts
        if concept.term == "attention"
    )

    assert attention.frequency == 3
    assert attention.sections == ["Introduction"]
    assert attention.contexts
    assert attention.score > 0


def test_minimum_frequency():
    sections = [
        DocumentSection(
            heading="Introduction",
            text="Transformer attention architecture.",
        ),
    ]

    concepts = extract_concepts(
        sections,
        min_frequency=2,
    )

    assert concepts == []


def test_multi_word_concept_gets_score():
    sections = [
        DocumentSection(
            heading="Attention",
            text=(
                "self attention improves sequence modeling. "
                "self attention is efficient."
            ),
        ),
    ]

    concepts = extract_concepts(
        sections,
        min_frequency=2,
    )

    self_attention = next(
        concept
        for concept in concepts
        if concept.term == "self attention"
    )

    assert self_attention.frequency == 2
    assert self_attention.sections == ["Attention"]
    assert self_attention.score > 0


def test_common_words_are_filtered():
    sections = [
        DocumentSection(
            heading="Introduction",
            text=(
                "the and our paper work arxiv "
                "attention attention"
            ),
        ),
    ]

    concepts = extract_concepts(
        sections,
        min_frequency=2,
    )

    terms = {concept.term for concept in concepts}

    assert "the" not in terms
    assert "and" not in terms
    assert "our" not in terms
    assert "paper" not in terms
    assert "arxiv" not in terms
    assert "attention" in terms