from unknown_finder.gaps.models import Gap


def build_hypothesis_prompt(gap: Gap) -> str:
    return (
        "Generate one scientifically testable hypothesis connecting "
        f"the concepts '{gap.concept_a}' and '{gap.concept_b}'. "
        f"The detected gap confidence is {gap.confidence}. "
        "Return a concise testable hypothesis."
    )

from unknown_finder.evaluation.ollama_client import OllamaClient


def generate_hypothesis(gap: Gap) -> str:
    client = OllamaClient()
    prompt = build_hypothesis_prompt(gap)
    return client.generate(prompt)

from unknown_finder.hypothesis.models import Hypothesis


def generate_hypothesis_model(
    gap: Gap,
    evidence_ids: list[str] | None = None,
) -> Hypothesis:
    generated_text = generate_hypothesis(gap)

    return Hypothesis(
        concept_a=gap.concept_a,
        concept_b=gap.concept_b,
        evidence_ids=evidence_ids or [],
        confidence=gap.confidence,
        generated_text=generated_text,
    )
