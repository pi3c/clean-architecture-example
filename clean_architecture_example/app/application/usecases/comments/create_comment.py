from app.application.common.date_time_provider import DateTimeProvider
from app.application.common.id_provider import IdProvider
from app.application.common.interactor import Interactor
from app.application.common.unit_of_work import UnitOfWork
from app.application.contracts.comments.comment_details_response import (
    CommentDetailsResponse,
)
from app.application.contracts.comments.create_comment_request import (
    CreateCommentRequest,
)
from app.domain.comments.comment import Comment
from app.domain.comments.repository import CommentRepository
from app.domain.posts.error import PostNotFoundError
from app.domain.posts.post import PostId
from app.domain.posts.repository import PostRepository


class CreateComment(Interactor[CreateCommentRequest, CommentDetailsResponse]):
    def __init__(
        self,
        uow: UnitOfWork,
        id_provider: IdProvider,
        post_repository: PostRepository,
        date_time_provider: DateTimeProvider,
        comment_repository: CommentRepository,
    ) -> None:
        self.uow = uow
        self.id_provider = id_provider
        self.post_repository = post_repository
        self.date_time_provider = date_time_provider
        self.comment_repository = comment_repository

    async def __call__(self, request: CreateCommentRequest) -> CommentDetailsResponse:
        post = await self.post_repository.find_by_id(PostId(request.post_id))

        if post is None:
            raise PostNotFoundError(f"Post with id {request.post_id} not found")

        user_id = self.id_provider.get_current_user_id()

        comment = Comment.create(
            owner_id=user_id.value,
            content=request.content,
            post_id=request.post_id,
            created_at=self.date_time_provider.get_current_time(),
            updated_at=self.date_time_provider.get_current_time(),
        )

        await self.comment_repository.create(comment)
        await self.uow.commit()

        return CommentDetailsResponse(
            id=comment.id.value,
            content=comment.content.value,
            post_id=comment.post_id.value,
            owner_id=comment.owner_id.value,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
