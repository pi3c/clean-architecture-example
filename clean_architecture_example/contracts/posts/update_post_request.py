from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True)
class UpdatePostRequest:
    title: str
    content: str | None = field(default=None)

    @property
    def id(self) -> UUID:
        return getattr(self, "__id", None)

    @id.setter
    def id(self, value: UUID) -> None:
        setattr(self, "__id", value)
