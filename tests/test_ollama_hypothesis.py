from unknown_finder.evaluation.ollama_hypothesis import build_hypothesis_prompt, generate_hypothesis, generate_hypothesis_model
from unknown_finder.gaps.models import Gap
from unknown_finder.hypothesis.models import Hypothesis


def test_build_hypothesis_prompt_includes_gap_concepts():
    prompt = build_hypothesis_prompt(
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
            confidence=0.8,
        )
    )

    assert "attention" in prompt
    assert "medical imaging" in prompt
    assert "0.8" in prompt
    assert "testable hypothesis" in prompt.lower()



def test_generate_hypothesis_uses_ollama_client(monkeypatch):
    calls = []

    class FakeClient:
        def generate(self, prompt):
            calls.append(prompt)
            return "Attention mechanisms improve medical image analysis."

    monkeypatch.setattr(
        "unknown_finder.evaluation.ollama_hypothesis.OllamaClient",
        FakeClient,
    )

    result = generate_hypothesis(
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
        )
    )

    assert result == "Attention mechanisms improve medical image analysis."
    assert len(calls) == 1
    assert "attention" in calls[0]
    assert "medical imaging" in calls[0]



def test_generate_hypothesis_model_returns_hypothesis(monkeypatch):
    monkeypatch.setattr(
        "unknown_finder.evaluation.ollama_hypothesis.OllamaClient",
        lambda: type(
            "FakeClient",
            (),
            {
                "generate": lambda self, prompt:
                "Attention mechanisms improve medical image analysis."
            },
        )(),
    )

    gap = Gap(
        concept_a="attention",
        concept_b="medical imaging",
        confidence=0.8,
    )

    result = generate_hypothesis_model(
        gap,
        evidence_ids=["evidence-001"],
    )

    assert isinstance(result, Hypothesis)
    assert result.concept_a == "attention"
    assert result.concept_b == "medical imaging"
    assert result.confidence == 0.8
    assert result.evidence_ids == ["evidence-001"]
    assert result.generated_text == (
        "Attention mechanisms improve medical image analysis."
    )
