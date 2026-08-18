from pathlib import Path

import httpx


class PaperDownloader:
    def download(self, url: str, destination: str | Path) -> Path:
        destination = Path(destination)

        response = httpx.get(
            url,
            timeout=60.0,
            follow_redirects=True,
        )
        response.raise_for_status()

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(response.content)

        return destination