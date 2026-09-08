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
