from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True)
class GetCommentsRequest:
    limit: int = field(default=20)
    offset: int = field(default=0)


@dataclass(frozen=True)
class GetCommentsByPostIdRequest:
    post_id: UUID
    limit: int = field(default=20)
    offset: int = field(default=0)
