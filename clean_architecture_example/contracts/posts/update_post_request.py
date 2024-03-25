from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class UpdatePostRequest:
    title: str
    content: str | None = field(default=None)
    __id: UUID | None = field(default=None, init=False)

    @property
    def id(self) -> UUID:
        return getattr(self, "__id", None)

    @id.setter
    def id(self, value: UUID) -> None:
        setattr(self, "__id", value)
