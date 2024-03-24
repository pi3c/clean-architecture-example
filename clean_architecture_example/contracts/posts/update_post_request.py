from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True)
class UpdatePostRequest:
    id: UUID
    title: str
    content: str | None = field(default=None)
