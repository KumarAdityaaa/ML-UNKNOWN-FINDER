import re

from .models import DocumentSection


SECTION_NUMBER_PATTERN = re.compile(
    r"^\d+(?:\.\d+)*\.?$"
)

NUMBERED_HEADING_PATTERN = re.compile(
    r"^(?P<number>\d+(?:\.\d+)*)\s+"
    r"(?P<heading>[A-Z][A-Za-z0-9 ,:&'()/\-]{2,80})$"
)

NAMED_HEADING_PATTERN = re.compile(
    r"^(?P<heading>"
    r"abstract|introduction|background|related work|"
    r"methods?|methodology|materials and methods|"
    r"experiments?|evaluation|results?|analysis|"
    r"discussion|limitations?|future work|"
    r"conclusions?|acknowledg(?:e)?ments?|references"
    r")$",
    re.IGNORECASE,
)


def _is_likely_heading(line: str) -> tuple[str, int] | None:
    line = line.strip()

    if not line:
        return None

    numbered = NUMBERED_HEADING_PATTERN.match(line)

    if numbered:
        number = numbered.group("number")
        heading = numbered.group("heading").strip()

        if len(heading.split()) > 12:
            return None

        if heading.endswith((".", ",", ";", ":")):
            return None

        level = number.count(".") + 1

        return heading, level

    named = NAMED_HEADING_PATTERN.match(line)

    if named:
        return named.group("heading").strip().title(), 1

    return None


def detect_sections(text: str) -> list[DocumentSection]:
    sections: list[DocumentSection] = []

    current_heading = "Document Text"
    current_level = 1
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines

        content = "\n".join(current_lines).strip()

        if content:
            sections.append(
                DocumentSection(
                    heading=current_heading,
                    text=content,
                    level=current_level,
                )
            )

        current_lines = []

    lines = text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].strip()

        if not line:
            current_lines.append(lines[index])
            index += 1
            continue

        # Handle PDF extraction where section number and
        # heading are separated into two lines:
        #
        # 3.1
        # Encoder and Decoder Stacks
        if SECTION_NUMBER_PATTERN.match(line) and index + 1 < len(lines):
            next_line = lines[index + 1].strip()

            combined = f"{line} {next_line}"
            detected = _is_likely_heading(combined)

            if detected:
                heading, level = detected

                flush()

                current_heading = heading
                current_level = level

                index += 2
                continue

        detected = _is_likely_heading(line)

        if detected:
            heading, level = detected

            flush()

            current_heading = heading
            current_level = level
        else:
            current_lines.append(lines[index])

        index += 1

    flush()

    return sections