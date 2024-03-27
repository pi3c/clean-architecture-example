from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateCommentRequest:
    id: UUID
    content: str
