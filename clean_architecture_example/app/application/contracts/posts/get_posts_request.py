from dataclasses import dataclass, field


@dataclass(frozen=True)
class GetPostListRequest:
    limit: int = field(default=20)
    offset: int = field(default=0)
