from pathlib import Path

import httpx

from .retry import with_retries


class PaperDownloader:
    def download(self, url: str, destination: str | Path) -> Path:
        destination = Path(destination)

        def fetch() -> bytes:
            response = httpx.get(
                url,
                timeout=60.0,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response.content

        content = with_retries(fetch)

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)

        return destination