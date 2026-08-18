import json
from pathlib import Path

from .models import PaperRecord


class CorpusRegistry:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(self, papers: list[PaperRecord]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        data = [paper.model_dump(mode="json") for paper in papers]

        self.path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def load(self) -> list[PaperRecord]:
        if not self.path.exists():
            return []

        data = json.loads(self.path.read_text(encoding="utf-8"))

        return [PaperRecord.model_validate(item) for item in data]