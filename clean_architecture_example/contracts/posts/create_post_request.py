from dataclasses import dataclass


@dataclass(frozen=True)
class CreatePostRequest:
    title: str
    content: str
