from contracts.comments.comment_details_response import CommentDetailsResponse
from contracts.comments.update_comment import UpdateCommentRequest
from core.application.common.date_time_provider import DateTimeProvider
from core.application.common.id_provider import IdProvider
from core.application.common.interactor import Interactor
from core.application.common.unit_of_work import UnitOfWork
from core.domain.comments.comment import CommentContent, CommentId
from core.domain.comments.error import CommentAccessDeniedError, CommentNotFoundError
from core.domain.comments.repository import CommentRepository


class UpdateComment(Interactor[UpdateCommentRequest, CommentDetailsResponse]):
    def __init__(
        self,
        uow: UnitOfWork,
        id_provider: IdProvider,
        comment_repository: CommentRepository,
        date_time_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.id_provider = id_provider
        self.comment_repository = comment_repository
        self.date_time_provider = date_time_provider

    async def __call__(self, request: UpdateCommentRequest) -> CommentDetailsResponse:
        comment = await self.comment_repository.find_by_id(CommentId(request.id))

        if comment is None:
            raise CommentNotFoundError(f"Comment with id {request.id} not found")

        user_id = self.id_provider.get_current_user_id()

        if comment.owner_id != user_id:
            raise CommentAccessDeniedError("You are not the owner of this comment")

        updated_at = self.date_time_provider.get_current_time()

        await self.comment_repository.update(
            comment.id, updated_at=updated_at, content=CommentContent(request.content)
        )

        await self.uow.commit()

        return CommentDetailsResponse(
            id=comment.id.value,
            content=request.content,
            post_id=comment.post_id.value,
            owner_id=comment.owner_id.value,
            created_at=comment.created_at,
            updated_at=updated_at,
        )
