import re

from .models import Reference


REFERENCE_PATTERN = re.compile(
    r"^\[(?P<id>\d+)\]\s*(?P<text>.+)$"
)


def _get_references_text(text: str) -> str:
    lines = text.splitlines()

    for index, line in enumerate(lines):
        if line.strip().lower() == "references":
            return "\n".join(lines[index + 1:])

    return ""


def extract_references(text: str) -> list[Reference]:
    references: list[Reference] = []

    references_text = _get_references_text(text)

    if not references_text:
        return references

    lines = references_text.splitlines()

    current_id: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_id, current_lines

        if current_id is not None and current_lines:
            reference_text = " ".join(
                line.strip()
                for line in current_lines
                if line.strip()
            ).strip()

            if reference_text:
                references.append(
                    Reference(
                        reference_id=current_id,
                        text=reference_text,
                    )
                )

        current_id = None
        current_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        match = REFERENCE_PATTERN.match(line)

        if match:
            flush()

            current_id = match.group("id")
            current_lines = [match.group("text")]
        elif current_id is not None:
            current_lines.append(line)

    flush()

    return references