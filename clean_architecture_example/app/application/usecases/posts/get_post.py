from uuid import UUID

from app.application.common.interactor import Interactor
from app.application.contracts.posts.get_posts_request import GetPostListRequest
from app.application.contracts.posts.post_details_response import PostDetailsResponse
from app.application.contracts.posts.post_list_response import PostListResponse
from app.domain.posts.error import PostNotFoundError
from app.domain.posts.repository import PostRepository
from app.domain.users.user import UserId


class GetPostById(Interactor[UUID, PostDetailsResponse]):
    def __init__(self, post_repository: PostRepository) -> None:
        self.post_repository = post_repository

    async def __call__(self, request: UUID) -> PostDetailsResponse:
        post = await self.post_repository.find_by_id(UserId(request))  # type: ignore

        if post is None:
            raise PostNotFoundError(f"Post with id {request} not found")

        return PostDetailsResponse(
            id=post.id.value,
            title=post.title.value,
            content=post.content.value,
            owner_id=post.owner_id.value,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )


class GetPostList(Interactor[GetPostListRequest, PostListResponse]):
    def __init__(self, post_repository: PostRepository) -> None:
        self.post_repository = post_repository

    async def __call__(self, request: GetPostListRequest) -> PostListResponse:
        posts = await self.post_repository.find_all(request.limit, request.offset)

        if not posts:
            return PostListResponse([], 0)

        data = [
            PostDetailsResponse(
                id=post.id.value,
                title=post.title.value,
                content=post.content.value,
                owner_id=post.owner_id.value,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            for post in posts
        ]

        return PostListResponse(data, len(data))
