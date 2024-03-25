from contracts.posts.post_details_response import PostDetailsResponse
from contracts.posts.update_post_request import UpdatePostRequest
from core.application.common.date_time_provider import DateTimeProvider
from core.application.common.id_provider import IdProvider
from core.application.common.interactor import Interactor
from core.application.common.unit_of_work import UnitOfWork
from core.domain.posts.error import PostAccessDeniedError, PostNotFoundError
from core.domain.posts.post import PostContent, PostId, PostTitle
from core.domain.posts.repository import PostRepository


class UpdatePost(Interactor[UpdatePostRequest, PostDetailsResponse]):
    def __init__(
        self,
        uow: UnitOfWork,
        id_provider: IdProvider,
        post_repository: PostRepository,
        date_time_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.id_provider = id_provider
        self.post_repository = post_repository
        self.date_time_provider = date_time_provider

    async def __call__(self, request: UpdatePostRequest) -> PostDetailsResponse:
        user_id = self.id_provider.get_current_user_id()

        post = await self.post_repository.find_by_id(PostId(request.id))

        if post is None:
            raise PostNotFoundError(f"Post with id {request.id} not found")

        if post.owner_id != user_id:
            raise PostAccessDeniedError("You are not the owner of this post")

        updated_at = self.date_time_provider.get_current_time()

        if not request.content:
            content = None
        else:
            content = PostContent(request.content)

        await self.post_repository.update(
            post.id,
            content=content,
            updated_at=updated_at,
            title=PostTitle(request.title),
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
