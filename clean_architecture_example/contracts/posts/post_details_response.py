from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class PostDetailsResponse:
    id: UUID
    title: str
    content: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
