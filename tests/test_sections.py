from unknown_finder.parsing.sections import detect_sections


def test_detect_sections():
    text = """
1 Introduction

Scientific research requires careful analysis.

2 Methods

We collected data from several sources.

3 Results

The proposed method improved performance.

4 Conclusion

The results demonstrate the usefulness of the approach.

References

[1] Example reference.
"""

    sections = detect_sections(text)

    assert len(sections) == 5

    assert sections[0].heading == "Introduction"
    assert "careful analysis" in sections[0].text

    assert sections[1].heading == "Methods"
    assert "collected data" in sections[1].text

    assert sections[2].heading == "Results"
    assert "improved performance" in sections[2].text

    assert sections[3].heading == "Conclusion"
    assert "usefulness" in sections[3].text

    assert sections[4].heading == "References"
    assert "Example reference" in sections[4].text


def test_detect_sections_without_numbering():
    text = """
Abstract

This is the abstract.

Introduction

This is the introduction.

Discussion

This is the discussion.
"""

    sections = detect_sections(text)

    assert len(sections) == 3
    assert sections[0].heading == "Abstract"
    assert sections[1].heading == "Introduction"
    assert sections[2].heading == "Discussion"

def test_real_paper_section_hierarchy():
    text = """
1
Introduction

This is the introduction.

3
Model Architecture

This describes the architecture.

3.1
Encoder and Decoder Stacks

The encoder and decoder are described here.

3.2
Attention

Attention mechanisms are described here.

3.2.1
Scaled Dot-Product Attention

Scaled dot-product attention is described here.

3.2.2
Multi-Head Attention

Multi-head attention is described here.

6
Results

Experimental results are presented here.

6.1
Machine Translation

Translation results are presented here.

References

[1] Example reference.
"""

    sections = detect_sections(text)

    assert [section.heading for section in sections] == [
        "Introduction",
        "Model Architecture",
        "Encoder and Decoder Stacks",
        "Attention",
        "Scaled Dot-Product Attention",
        "Multi-Head Attention",
        "Results",
        "Machine Translation",
        "References",
    ]

    assert [section.level for section in sections] == [
        1,
        1,
        2,
        2,
        3,
        3,
        1,
        2,
        1,
    ]
