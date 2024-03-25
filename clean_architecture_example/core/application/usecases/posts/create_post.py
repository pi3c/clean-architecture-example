from contracts.posts.create_post_request import CreatePostRequest
from contracts.posts.post_details_response import PostDetailsResponse
from core.application.common.date_time_provider import DateTimeProvider
from core.application.common.interactor import Interactor
from core.application.common.unit_of_work import UnitOfWork
from core.application.common.id_provider import IdProvider
from core.domain.posts.post import Post
from core.domain.posts.repository import PostRepository


class CreatePost(Interactor[CreatePostRequest, PostDetailsResponse]):
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

    async def __call__(self, request: CreatePostRequest) -> PostDetailsResponse:
        user_id = self.id_provider.get_current_user_id()

        post = Post.create(
            owner_id=user_id,
            title=request.title,
            content=request.content,
            created_at=self.date_time_provider.get_current_time(),
            updated_at=self.date_time_provider.get_current_time(),
        )
        await self.post_repository.create(post)

        await self.uow.commit()

        return PostDetailsResponse(
            id=post.id.value,
            title=post.title.value,
            content=post.content.value,
            owner_id=post.owner_id.value,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
