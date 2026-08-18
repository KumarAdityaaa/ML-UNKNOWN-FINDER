from dataclasses import dataclass


@dataclass(frozen=True)
class IngestionEvaluationCase:
    query: str
    expected_sources: set[str]


def evaluate_sources(
    cases: list[IngestionEvaluationCase],
    actual_sources: dict[str, set[str]],
) -> float:
    if not cases:
        return 0.0

    scores = []

    for case in cases:
        expected = case.expected_sources
        actual = actual_sources.get(case.query, set())

        if not expected:
            scores.append(1.0 if not actual else 0.0)
            continue

        scores.append(len(expected & actual) / len(expected))

    return sum(scores) / len(scores)