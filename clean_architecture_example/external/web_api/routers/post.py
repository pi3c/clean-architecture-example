from typing import Annotated

from contracts.posts.create_post_request import CreatePostRequest
from contracts.posts.get_posts_request import GetPostByIdRequest, GetPostListRequest
from contracts.posts.post_details_response import PostDetailsResponse
from contracts.posts.post_list_response import PostListResponse
from contracts.posts.update_post_request import UpdatePostRequest
from core.application.usecases.posts.create_post import CreatePost
from core.application.usecases.posts.get_posts import GetPostById, GetPostList
from core.application.usecases.posts.update_post import UpdatePost
from external.web_api.authentication.jwt_auth import authentication_required
from external.web_api.extensions.rate_limit import limiter

from fastapi import APIRouter, Depends, Request
from dishka.integrations.fastapi import DishkaRoute, FromDishka

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    route_class=DishkaRoute,
)


@post_router.get("/", response_model=PostListResponse)
@limiter.limit("3/minute")
async def get_post_list(
    request: Request,
    get_post_list_request: Annotated[GetPostListRequest, Depends()],
    get_post_list_interactor: Annotated[GetPostList, FromDishka()],
) -> PostListResponse:
    return await get_post_list_interactor(get_post_list_request)


@post_router.post(
    "/",
    response_model=PostDetailsResponse,
    dependencies=[Depends(authentication_required)],
)
@limiter.limit("3/minute")
async def create_post(
    request: Request,
    create_post_request: CreatePostRequest,
    create_post_interactor: Annotated[CreatePost, FromDishka()],
) -> PostDetailsResponse:
    return await create_post_interactor(create_post_request)


@post_router.patch(
    "/",
    response_model=PostDetailsResponse,
    dependencies=[Depends(authentication_required)],
)
@limiter.limit("3/minute")
async def update_post(
    request: Request,
    update_post_request: UpdatePostRequest,
    update_post_interactor: Annotated[UpdatePost, FromDishka()],
) -> PostDetailsResponse:
    return await update_post_interactor(update_post_request)


@post_router.get("/{post_id}", response_model=PostDetailsResponse)
@limiter.limit("3/minute")
async def get_post_by_id(
    request: Request,
    get_post_request: Annotated[GetPostByIdRequest, Depends()],
    get_post_interactor: Annotated[GetPostById, FromDishka()],
) -> PostDetailsResponse:
    return await get_post_interactor(get_post_request)
