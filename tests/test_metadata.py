from unknown_finder.parsing.metadata import (
    extract_abstract,
    extract_authors,
    extract_metadata,
    extract_title,
)


SAMPLE_TEXT = """
Attention Is All You Need

Ashish Vaswani∗
Google Brain
avaswani@google.com

Noam Shazeer∗
Google Brain
noam@google.com

Abstract

The Transformer is a new simple network architecture based solely on attention mechanisms.

1 Introduction

Sequence models are widely used in machine translation.
"""


def test_extract_title():
    assert extract_title(SAMPLE_TEXT) == "Attention Is All You Need"


def test_extract_authors():
    authors = extract_authors(SAMPLE_TEXT)

    assert "Ashish Vaswani" in authors
    assert "Noam Shazeer" in authors


def test_extract_abstract():
    abstract = extract_abstract(SAMPLE_TEXT)

    assert "Transformer" in abstract
    assert "attention mechanisms" in abstract
    assert "Sequence models" not in abstract


def test_extract_metadata():
    metadata = extract_metadata(SAMPLE_TEXT)

    assert metadata["title"] == "Attention Is All You Need"
    assert "Ashish Vaswani" in metadata["authors"]
    assert "Noam Shazeer" in metadata["authors"]
    assert "Transformer" in metadata["abstract"]