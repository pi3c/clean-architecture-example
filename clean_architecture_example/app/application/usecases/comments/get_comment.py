from uuid import UUID

from app.application.common.interactor import Interactor
from app.application.contracts.comments.comment_details_response import (
    CommentDetailsResponse,
)
from app.application.contracts.comments.comment_list_response import CommentListResponse
from app.application.contracts.comments.get_comments_request import (
    GetCommentsByPostIdRequest,
)
from app.domain.comments.comment import Comment, CommentId
from app.domain.comments.error import CommentNotFoundError
from app.domain.comments.repository import CommentRepository
from app.domain.posts.post import PostId


class GetCommentById(Interactor[UUID, CommentDetailsResponse]):
    def __init__(self, comment_repository: CommentRepository) -> None:
        self.comment_repository = comment_repository

    async def __call__(self, request: UUID) -> CommentDetailsResponse:
        comment = await self.comment_repository.find_by_id(CommentId(request))

        if comment is None:
            raise CommentNotFoundError(f"Comment with id {request} not found")

        return CommentDetailsResponse(
            id=request,
            content=comment.content.value,
            post_id=comment.post_id.value,
            owner_id=comment.owner_id.value,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


class GetCommentListByPostId(Interactor[GetCommentsByPostIdRequest, CommentListResponse]):
    def __init__(self, comment_repository: CommentRepository) -> None:
        self.comment_repository = comment_repository

    async def __call__(self, request: GetCommentsByPostIdRequest) -> CommentListResponse:
        comments = await self.comment_repository.find_by_post_id(
            PostId(request.post_id),
            request.limit,
            request.offset,
        )

        if not comments:
            return CommentListResponse([], 0)

        def to_response(comment: Comment) -> CommentDetailsResponse:
            return CommentDetailsResponse(
                id=comment.id.value,
                content=comment.content.value,
                post_id=comment.post_id.value,
                owner_id=comment.owner_id.value,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
            )

        data = [to_response(comment) for comment in comments]

        return CommentListResponse(data, len(data))
