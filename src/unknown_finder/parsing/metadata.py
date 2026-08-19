import re

from .models import ParsedDocument


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _is_author_like(line: str) -> bool:
    line = line.strip().rstrip("∗†‡")

    if not line:
        return False

    if EMAIL_PATTERN.match(line):
        return True

    if re.search(
        r"\b("
        r"university|college|institute|google|research|"
        r"brain|laboratory|lab|department|school"
        r")\b",
        line,
        re.IGNORECASE,
    ):
        return True

    words = line.split()

    if not 2 <= len(words) <= 6:
        return False

    return all(
        re.match(r"^[A-ZÀ-ÖØ-Ý][A-Za-zÀ-ÖØ-öø-ÿ.'\-]*[∗†‡]?$", word)
        for word in words
    )


def extract_title(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for index, line in enumerate(lines):
        if line.lower() == "abstract":
            candidates = lines[:index]

            for candidate in candidates:
                if len(candidate.split()) < 3:
                    continue

                if len(candidate) > 200:
                    continue

                if re.search(
                    r"\b("
                    r"permission|attribution|reproduce|journalistic|"
                    r"scholarly works|copyright|license|grants permission"
                    r")\b",
                    candidate,
                    re.IGNORECASE,
                ):
                    continue

                if EMAIL_PATTERN.match(candidate):
                    continue

                # Skip affiliations and obvious author metadata.
                if re.search(
                    r"\b("
                    r"university|college|institute|google|research|"
                    r"brain|laboratory|lab|department|school"
                    r")\b",
                    candidate,
                    re.IGNORECASE,
                ):
                    continue

                # Skip lines that look like email addresses or
                # short person-name entries.
                if re.fullmatch(
                    r"[A-ZÀ-ÖØ-Ý][A-Za-zÀ-ÖØ-öø-ÿ.'\-]+"
                    r"(?:\s+[A-ZÀ-ÖØ-Ý][A-Za-zÀ-ÖØ-öø-ÿ.'\-]+){1,2}[∗†‡]?",
                    candidate,
                ):
                    continue

                return candidate

            break

    return ""


def extract_authors(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    authors = []

    for line in lines:
        if line.lower() == "abstract":
            break

        if "@" in line:
            continue

        cleaned = line.rstrip("∗†‡")

        if re.fullmatch(
            r"[A-ZÀ-ÖØ-Ý][A-Za-zÀ-ÖØ-öø-ÿ.'\-]+"
            r"(?:\s+[A-ZÀ-ÖØ-Ý][A-Za-zÀ-ÖØ-öø-ÿ.'\-]+){1,4}",
            cleaned,
        ):
            authors.append(cleaned)

    return authors


def extract_abstract(text: str) -> str:
    lines = text.splitlines()

    start = None

    for index, line in enumerate(lines):
        if line.strip().lower() == "abstract":
            start = index + 1
            break

    if start is None:
        return ""

    abstract_lines = []

    for line in lines[start:]:
        if line.strip().lower() in {
            "introduction",
            "1 introduction",
        }:
            break

        abstract_lines.append(line.strip())

    return " ".join(
        line for line in abstract_lines if line
    ).strip()


def extract_metadata(text: str) -> dict:
    return {
        "title": extract_title(text),
        "authors": extract_authors(text),
        "abstract": extract_abstract(text),
    }