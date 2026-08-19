import re

from .models import Citation


CITATION_PATTERN = re.compile(
    r"\[(?P<ids>\d+(?:\s*,\s*\d+)*)\]"
)


def extract_citations(text: str) -> list[Citation]:
    citations: list[Citation] = []

    lines = text.splitlines()

    for index, line in enumerate(lines):
        for match in CITATION_PATTERN.finditer(line):
            context_start = max(0, index - 1)
            context_end = min(len(lines), index + 2)

            context = " ".join(
                current.strip()
                for current in lines[context_start:context_end]
                if current.strip()
            )

            for reference_id in re.split(
                r"\s*,\s*",
                match.group("ids"),
            ):
                citations.append(
                    Citation(
                        reference_id=reference_id,
                        context=context,
                    )
                )

    return citations