from unknown_finder.parsing.references import extract_references


def test_extract_references():
    text = """
References

[1] Vaswani, A. et al. Attention Is All You Need.

[2] Bahdanau, D., Cho, K. and Bengio, Y.
Neural Machine Translation by Jointly Learning to Align and Translate.

[3] Sutskever, I., Vinyals, O. and Le, Q. V.
Sequence to Sequence Learning with Neural Networks.
"""

    references = extract_references(text)

    assert len(references) == 3

    assert references[0].reference_id == "1"
    assert "Attention Is All You Need" in references[0].text

    assert references[1].reference_id == "2"
    assert "Neural Machine Translation" in references[1].text

    assert references[2].reference_id == "3"
    assert "Sequence to Sequence Learning" in references[2].text


def test_extract_references_empty():
    references = extract_references(
        "This document contains no references."
    )

    assert references == []