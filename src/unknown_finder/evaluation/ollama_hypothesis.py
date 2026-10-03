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

def generate_hypotheses(gap: Gap) -> list[str]:
    client = OllamaClient()
    prompt = (
        f"Given a research gap between '{gap.concept_a}' and "
        f"'{gap.concept_b}', return exactly 3 numbered testable hypotheses."
    )
    response = client.generate(prompt)

    hypotheses = []
    for line in response.splitlines():
        line = line.strip()
        if len(line) >= 3 and line[0].isdigit() and line[1] == ".":
            hypotheses.append(line[2:].strip())

    return hypotheses
