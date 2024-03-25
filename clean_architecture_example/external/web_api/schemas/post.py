from dataclasses import dataclass, field


@dataclass(frozen=True)
class UpdatePostSchema:
    title: str
    content: str | None = field(default=None)
