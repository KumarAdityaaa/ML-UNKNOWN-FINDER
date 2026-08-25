from unknown_finder.gaps.detector import detect_gaps
from unknown_finder.gaps.models import Gap
import pytest

def test_detect_gap_from_underexplored_concept_pair():
    gaps = detect_gaps(
        [
            ("attention", "medical imaging"),
        ]
    )

    assert len(gaps) == 1

    gap = gaps[0]

    assert isinstance(gap, Gap)
    assert gap.concept_a == "attention"
    assert gap.concept_b == "medical imaging"

def test_detect_gaps_removes_duplicate_pairs():
    gaps = detect_gaps(
        [
            ("attention", "medical imaging"),
            ("attention", "medical imaging"),
        ]
    )

    assert len(gaps) == 1
    assert gaps[0].concept_a == "attention"
    assert gaps[0].concept_b == "medical imaging"

def test_detect_gaps_treats_reverse_pairs_as_same_gap():
    gaps = detect_gaps(
        [
            ("attention", "medical imaging"),
            ("medical imaging", "attention"),
        ]
    )

    assert len(gaps) == 1
    assert gaps[0].concept_a == "attention"
    assert gaps[0].concept_b == "medical imaging"

def test_detect_gaps_with_no_pairs_returns_empty():
    gaps = detect_gaps([])

    assert gaps == []

def test_detect_gaps_ignores_self_pairs():
    gaps = detect_gaps(
        [
            ("attention", "attention"),
        ]
    )

    assert gaps == []

def test_gap_has_confidence():
    gaps = detect_gaps(
        [
            ("attention", "medical imaging"),
        ]
    )

    assert len(gaps) == 1
    assert gaps[0].confidence == 1.0

def test_gap_rejects_invalid_confidence():

    with pytest.raises(ValueError):
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
            confidence=1.5,
        )

def test_gap_rejects_negative_confidence():

    with pytest.raises(ValueError):
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
            confidence=-0.1,
        )

def test_gap_accepts_confidence_boundaries():
    gap_zero = Gap(
        concept_a="attention",
        concept_b="medical imaging",
        confidence=0.0,
    )

    gap_one = Gap(
        concept_a="attention",
        concept_b="medical imaging",
        confidence=1.0,
    )

    assert gap_zero.confidence == 0.0
    assert gap_one.confidence == 1.0

def test_detect_gaps_keeps_highest_confidence_for_duplicate_pair():
    gaps = detect_gaps(
        [
            ("attention", "medical imaging", 0.4),
            ("medical imaging", "attention", 0.9),
        ]
    )

    assert len(gaps) == 1
    assert gaps[0].confidence == 0.9