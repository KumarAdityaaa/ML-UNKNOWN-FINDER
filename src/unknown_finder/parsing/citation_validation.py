from .models import Citation, Reference


def validate_citations(
    citations: list[Citation],
    references: list[Reference],
) -> list[Citation]:
    """
    Return only citations whose reference IDs exist
    in the extracted reference list.
    """

    reference_ids = {
        reference.reference_id
        for reference in references
    }

    return [
        citation
        for citation in citations
        if citation.reference_id in reference_ids
    ]