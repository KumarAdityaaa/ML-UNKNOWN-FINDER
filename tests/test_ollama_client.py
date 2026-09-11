from unknown_finder.evaluation.ollama_client import OllamaClient
import unknown_finder.evaluation.ollama_client as ollama_client


def test_ollama_client_stores_model_name():
    client = OllamaClient(model="qwen2.5:7b")

    assert client.model == "qwen2.5:7b"


def test_ollama_client_generate_calls_ollama(monkeypatch):
    client = OllamaClient(model="qwen2.5:7b")

    class Result:
        stdout = "A research gap is an unexplored area."

    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))
        return Result()

    class FakeSubprocess:
        run = staticmethod(fake_run)

    monkeypatch.setattr(
        ollama_client,
        "subprocess",
        FakeSubprocess,
    )

    result = client.generate("What is a research gap?")

    assert result == "A research gap is an unexplored area."
    assert len(calls) == 1

import pytest


def test_ollama_client_rejects_empty_prompt():
    client = OllamaClient(model="qwen2.5:7b")

    with pytest.raises(ValueError):
        client.generate("")
