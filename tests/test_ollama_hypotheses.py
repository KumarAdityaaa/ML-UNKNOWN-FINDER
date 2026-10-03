from unknown_finder.evaluation.ollama_hypothesis import generate_hypotheses
from unknown_finder.gaps.models import Gap


def test_generate_hypotheses_returns_three_results(monkeypatch):
    monkeypatch.setattr(
        "unknown_finder.evaluation.ollama_hypothesis.OllamaClient",
        lambda: type(
            "FakeClient",
            (),
            {
                "generate": lambda self, prompt:
                "1. Test hypothesis one.\n"
                "2. Test hypothesis two.\n"
                "3. Test hypothesis three."
            },
        )(),
    )

    results = generate_hypotheses(
        Gap(
            concept_a="attention",
            concept_b="medical imaging",
        )
    )

    assert len(results) == 3
    assert results[0] == "Test hypothesis one."
    assert results[1] == "Test hypothesis two."
    assert results[2] == "Test hypothesis three."
