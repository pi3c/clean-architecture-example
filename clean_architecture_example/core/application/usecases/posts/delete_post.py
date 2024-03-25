from uuid import UUID
from core.application.common.interactor import Interactor
from core.application.common.unit_of_work import UnitOfWork
from core.application.common.user_context import UserContext
from core.domain.posts.error import PostAccessDeniedError, PostNotFoundError
from core.domain.posts.repository import PostRepository
from core.domain.users.user import UserId


class DeletePost(Interactor[UUID, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        user_context: UserContext,
        post_repository: PostRepository,
    ) -> None:
        self.uow = uow
        self.user_context = user_context
        self.post_repository = post_repository

    async def __call__(self, request: UUID) -> None:
        user = self.user_context.get_current_user()

        post = await self.post_repository.find_by_id(UserId(request))

        if not post:
            raise PostNotFoundError(f"Post with id {request} not found")

        if post.owner_id != user.id:
            raise PostAccessDeniedError("You are not the owner of this post")

        await self.post_repository.delete(post.id)

        await self.uow.commit()
