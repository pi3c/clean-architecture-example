from dataclasses import dataclass

from app.application.contracts.posts.post_details_response import PostDetailsResponse


@dataclass(frozen=True)
class PostListResponse:
    data: list[PostDetailsResponse]
    count: int
