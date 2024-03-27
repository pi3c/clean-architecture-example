from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CurrentUserResponse:
    id: UUID
    first_name: str
    last_name: str
    email: str
