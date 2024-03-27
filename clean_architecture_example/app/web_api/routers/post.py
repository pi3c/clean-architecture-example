from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from app.application.contracts.posts.create_post_request import CreatePostRequest
from app.application.contracts.posts.get_posts_request import GetPostListRequest
from app.application.contracts.posts.post_details_response import PostDetailsResponse
from app.application.contracts.posts.post_list_response import PostListResponse
from app.application.contracts.posts.update_post_request import UpdatePostRequest
from app.application.usecases.posts.create_post import CreatePost
from app.application.usecases.posts.delete_post import DeletePost
from app.application.usecases.posts.get_post import GetPostById, GetPostList
from app.application.usecases.posts.update_post import UpdatePost
from app.web_api.dependencies.authentication import auth_required
from app.web_api.schemas.post import UpdatePostSchema

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    route_class=DishkaRoute,
)


@post_router.get("/", response_model=PostListResponse)
async def get_post_list(
    get_post_list_request: Annotated[GetPostListRequest, Depends()],
    get_post_list_interactor: FromDishka[GetPostList],
) -> PostListResponse:
    return await get_post_list_interactor(get_post_list_request)


@post_router.post(
    "/",
    status_code=201,
    response_model=PostDetailsResponse,
    dependencies=[Depends(auth_required)],
)
async def create_post(
    create_post_request: CreatePostRequest,
    create_post_interactor: FromDishka[CreatePost],
) -> PostDetailsResponse:
    return await create_post_interactor(create_post_request)


@post_router.get("/{post_id}", response_model=PostDetailsResponse)
async def get_post_by_id(
    post_id: UUID,
    get_post_interactor: FromDishka[GetPostById],
) -> PostDetailsResponse:
    return await get_post_interactor(post_id)


@post_router.patch(
    "/{post_id}",
    response_model=PostDetailsResponse,
    dependencies=[Depends(auth_required)],
)
async def update_post(
    post_id: UUID,
    update_post_schema: UpdatePostSchema,
    update_post_interactor: FromDishka[UpdatePost],
) -> PostDetailsResponse:
    return await update_post_interactor(
        UpdatePostRequest(
            id=post_id,
            title=update_post_schema.title,
            content=update_post_schema.content,
        )
    )


@post_router.delete(
    "/{post_id}",
    status_code=204,
    dependencies=[Depends(auth_required)],
)
async def delete_post(
    post_id: UUID,
    delete_post_interactor: FromDishka[DeletePost],
) -> None:
    await delete_post_interactor(post_id)
