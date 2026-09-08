import math

from sklearn.feature_extraction.text import TfidfVectorizer


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("vectors must have the same length")

    norm_a = math.sqrt(sum(value * value for value in vector_a))
    norm_b = math.sqrt(sum(value * value for value in vector_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    dot_product = sum(
        left * right
        for left, right in zip(vector_a, vector_b)
    )

    return dot_product / (norm_a * norm_b)


def semantic_similarity(
    text_a: str,
    text_b: str,
) -> float:
    if not text_a.strip() or not text_b.strip():
        raise ValueError("texts must not be empty")

    vectorizer = TfidfVectorizer()

    matrix = vectorizer.fit_transform([text_a, text_b])

    return cosine_similarity(
        matrix[0].toarray()[0].tolist(),
        matrix[1].toarray()[0].tolist(),
    )
