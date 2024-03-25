from uuid import UUID

from core.application.common.id_provider import IdProvider
from core.application.common.interactor import Interactor
from core.application.common.unit_of_work import UnitOfWork
from core.domain.comments.comment import CommentId
from core.domain.comments.error import CommentAccessDeniedError, CommentNotFoundError
from core.domain.comments.repository import CommentRepository


class DeleteComment(Interactor[UUID, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        id_provider: IdProvider,
        comment_repository: CommentRepository,
    ) -> None:
        self.uow = uow
        self.id_provider = id_provider
        self.comment_repository = comment_repository

    async def __call__(self, request: UUID) -> None:
        comment = await self.comment_repository.find_by_id(CommentId(request))

        if not comment:
            raise CommentNotFoundError(f"Comment with id {request} not found")

        user_id = self.id_provider.get_current_user_id()

        if comment.owner_id != user_id:
            raise CommentAccessDeniedError("You are not the owner of this comment")

        await self.comment_repository.delete(comment.id)

        await self.uow.commit()
