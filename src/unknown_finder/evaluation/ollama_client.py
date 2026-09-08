import subprocess


class OllamaClient:
    def __init__(self, model: str = "qwen2.5:7b") -> None:
        if not model.strip():
            raise ValueError("model name must not be empty")

        self.model = model

    def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("prompt must not be empty")

        result = subprocess.run(
            ["ollama", "run", self.model, prompt],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()
