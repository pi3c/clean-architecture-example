from dataclasses import dataclass

from contracts.posts.post_details_response import PostDetailsResponse


@dataclass(frozen=True)
class PostListResponse:
    data: list[PostDetailsResponse]
    count: int
