from datetime import datetime, timezone

from pydantic import BaseModel


class PDFProvenance(BaseModel):
    paper_id: str
    source_url: str
    local_path: str
    downloaded_at: datetime

    @classmethod
    def create(
        cls,
        paper_id: str,
        source_url: str,
        local_path: str,
    ) -> "PDFProvenance":
        return cls(
            paper_id=paper_id,
            source_url=source_url,
            local_path=local_path,
            downloaded_at=datetime.now(timezone.utc),
        )