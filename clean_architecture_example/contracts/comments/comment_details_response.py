from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class CommentDetailsResponse:
    id: UUID
    content: str
    post_id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
