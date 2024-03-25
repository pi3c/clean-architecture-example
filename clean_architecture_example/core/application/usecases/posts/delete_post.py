from uuid import UUID
from core.application.common.interactor import Interactor
from core.application.common.unit_of_work import UnitOfWork
from core.application.common.id_provider import IdProvider
from core.domain.posts.error import PostAccessDeniedError, PostNotFoundError
from core.domain.posts.post import PostId
from core.domain.posts.repository import PostRepository


class DeletePost(Interactor[UUID, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        id_provider: IdProvider,
        post_repository: PostRepository,
    ) -> None:
        self.uow = uow
        self.id_provider = id_provider
        self.post_repository = post_repository

    async def __call__(self, request: UUID) -> None:
        user_id = self.id_provider.get_current_user_id()

        post = await self.post_repository.find_by_id(PostId(request))

        if not post:
            raise PostNotFoundError(f"Post with id {request} not found")

        if post.owner_id != user_id:
            raise PostAccessDeniedError("You are not the owner of this post")

        await self.post_repository.delete(post.id)

        await self.uow.commit()
