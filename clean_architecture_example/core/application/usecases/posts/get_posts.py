from contracts.posts.get_posts_request import (
    GetPostByIdRequest,
    GetPostListByOwnerIdRequest,
    GetPostListRequest,
)
from contracts.posts.post_details_response import PostDetailsResponse
from contracts.posts.post_list_response import PostListResponse
from core.application.common.interactor import Interactor
from core.domain.posts.error import PostNotFoundError
from core.domain.posts.post import PostId
from core.domain.posts.repository import PostRepository


class GetPostById(Interactor[GetPostByIdRequest, PostDetailsResponse]):
    def __init__(self, post_repository: PostRepository) -> None:
        self.post_repository = post_repository

    async def __call__(self, request: GetPostByIdRequest) -> PostDetailsResponse:
        post = await self.post_repository.find_by_id(PostId(request.id))

        if post is None:
            raise PostNotFoundError(f"Post with id {request.id} not found")

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
            return PostListResponse([])

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


class GetPostListByOwnerId(Interactor[GetPostListByOwnerIdRequest, PostListResponse]):
    def __init__(self, post_repository: PostRepository) -> None:
        self.post_repository = post_repository

    async def __call__(self, request: GetPostListByOwnerIdRequest) -> PostListResponse:
        posts = await self.post_repository.find_by_owner_id(
            request.owner_id, request.limit, request.offset
        )

        if not posts:
            return PostListResponse([])

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
