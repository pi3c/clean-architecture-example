from typing import Annotated
from uuid import UUID

from contracts.posts.create_post_request import CreatePostRequest
from contracts.posts.get_posts_request import GetPostListRequest
from contracts.posts.post_details_response import PostDetailsResponse
from contracts.posts.post_list_response import PostListResponse
from contracts.posts.update_post_request import UpdatePostRequest
from core.application.usecases.posts.create_post import CreatePost
from core.application.usecases.posts.delete_post import DeletePost
from core.application.usecases.posts.get_posts import GetPostById, GetPostList
from core.application.usecases.posts.update_post import UpdatePost
from external.web_api.authentication.jwt_auth import authentication_required

from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import DishkaRoute, FromDishka

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    route_class=DishkaRoute,
)


@post_router.get("/", response_model=PostListResponse)
async def get_post_list(
    get_post_list_request: Annotated[GetPostListRequest, Depends()],
    get_post_list_interactor: Annotated[GetPostList, FromDishka()],
) -> PostListResponse:
    return await get_post_list_interactor(get_post_list_request)


@post_router.post(
    "/",
    status_code=201,
    response_model=PostDetailsResponse,
    dependencies=[Depends(authentication_required)],
)
async def create_post(
    create_post_request: CreatePostRequest,
    create_post_interactor: Annotated[CreatePost, FromDishka()],
) -> PostDetailsResponse:
    return await create_post_interactor(create_post_request)


@post_router.get("/{post_id}", response_model=PostDetailsResponse)
async def get_post_by_id(
    post_id: UUID,
    get_post_interactor: Annotated[GetPostById, FromDishka()],
) -> PostDetailsResponse:
    return await get_post_interactor(post_id)


@post_router.patch(
    "/{post_id}",
    response_model=PostDetailsResponse,
    dependencies=[Depends(authentication_required)],
)
async def update_post(
    post_id: UUID,
    update_post_request: UpdatePostRequest,
    update_post_interactor: Annotated[UpdatePost, FromDishka()],
) -> PostDetailsResponse:
    update_post_request.id = post_id
    return await update_post_interactor(update_post_request)


@post_router.delete(
    "/{post_id}",
    status_code=204,
    dependencies=[Depends(authentication_required)],
)
async def delete_post(
    post_id: UUID,
    delete_post_interactor: Annotated[DeletePost, FromDishka()],
) -> None:
    await delete_post_interactor(post_id)
