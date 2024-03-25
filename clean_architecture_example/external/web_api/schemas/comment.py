from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateCommentSchema:
    content: str
