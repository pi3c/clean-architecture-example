from contracts.posts.post_details_response import PostDetailsResponse
from contracts.posts.update_post_request import UpdatePostRequest
from core.application.common.date_time_provider import DateTimeProvider
from core.application.common.interactor import Interactor
from core.application.common.unit_of_work import UnitOfWork
from core.application.common.user_context import UserContext
from core.domain.posts.error import PostAccessDeniedError, PostNotFoundError
from core.domain.posts.post import PostContent, PostId, PostTitle
from core.domain.posts.repository import PostRepository


class UpdatePost(Interactor[UpdatePostRequest, PostDetailsResponse]):
    def __init__(
        self,
        uow: UnitOfWork,
        user_context: UserContext,
        post_repository: PostRepository,
        date_time_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.user_context = user_context
        self.post_repository = post_repository
        self.date_time_provider = date_time_provider

    async def __call__(self, request: UpdatePostRequest) -> PostDetailsResponse:
        user = self.user_context.get_current_user()

        post = await self.post_repository.find_by_id(PostId(request.id))

        if post is None:
            raise PostNotFoundError(f"Post with id {request.id} not found")

        if post.owner_id.value != user.id.value:
            raise PostAccessDeniedError("You are not the owner of this post")

        updated_at = self.date_time_provider.get_current_time()

        await self.post_repository.edit(
            post.id,
            updated_at=updated_at,
            title=PostTitle(request.title),
            content=PostContent(request.content) if post.content else None,
        )

        await self.uow.commit()

        return PostDetailsResponse(
            id=post.id.value,
            title=request.title,
            content=request.content or post.content.value,
            owner_id=post.owner_id.value,
            created_at=post.created_at,
            updated_at=updated_at,
        )
