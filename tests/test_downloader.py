import httpx
import respx

from unknown_finder.ingestion.downloader import PaperDownloader


@respx.mock
def test_download(tmp_path):
    url = "https://example.org/paper.pdf"
    output = tmp_path / "paper.pdf"

    respx.get(url).mock(
        return_value=httpx.Response(
            200,
            content=b"%PDF-test-content",
        )
    )

    result = PaperDownloader().download(url, output)

    assert result == output
    assert output.exists()
    assert output.read_bytes() == b"%PDF-test-content"