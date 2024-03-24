from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from contracts.posts.create_post_request import CreatePostRequest
from contracts.posts.get_posts_request import GetPostByIdRequest, GetPostListRequest
from contracts.posts.post_details_response import PostDetailsResponse
from contracts.posts.post_list_response import PostListResponse
from core.application.usecases.posts.create_post import CreatePost
from core.application.usecases.posts.get_posts import GetPostById, GetPostList
from external.web_api.authentication.jwt_auth import authentication_required

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    route_class=DishkaRoute,
    dependencies=[Depends(authentication_required)],
)


@post_router.get("/", response_model=PostListResponse)
async def get_post_list(
    post_list_request: Annotated[GetPostListRequest, Depends()],
    post_interactor: Annotated[GetPostList, FromDishka()],
) -> PostListResponse:
    return await post_interactor(post_list_request)


@post_router.post("/", response_model=PostDetailsResponse)
async def create_post(
    create_post_request: CreatePostRequest,
    post_interactor: Annotated[CreatePost, FromDishka()],
) -> PostDetailsResponse:
    return await post_interactor(create_post_request)


@post_router.get("/{post_id}", response_model=PostDetailsResponse)
async def get_post_by_id(
    post_id: UUID,
    post_interactor: Annotated[GetPostById, FromDishka()],
) -> PostDetailsResponse:
    return await post_interactor(GetPostByIdRequest(post_id))
