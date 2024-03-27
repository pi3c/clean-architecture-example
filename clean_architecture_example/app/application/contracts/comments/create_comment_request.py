from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateCommentRequest:
    post_id: UUID
    content: str
