import httpx
import respx

from unknown_finder.ingestion.openalex import OpenAlexSource


MOCK_RESPONSE = {
    "results": [
        {
            "id": "https://openalex.org/W123",
            "title": "Test Machine Learning Paper",
            "authorships": [],
            "publication_date": "2026-01-01",
            "primary_location": {"source": None, "pdf_url": None},
            "doi": None,
        }
    ]
}


@respx.mock
def test_openalex_search():
    respx.get(OpenAlexSource.BASE_URL).mock(
        return_value=httpx.Response(200, json=MOCK_RESPONSE)
    )

    papers = OpenAlexSource().search("machine learning", limit=1)

    assert len(papers) == 1
    assert papers[0].title == "Test Machine Learning Paper"
    assert papers[0].openalex_id == "https://openalex.org/W123"