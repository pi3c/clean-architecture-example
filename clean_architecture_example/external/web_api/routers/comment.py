from typing import Annotated
from uuid import UUID

from contracts.comments.comment_details_response import CommentDetailsResponse
from contracts.comments.comment_list_response import CommentListResponse
from contracts.comments.create_comment_request import CreateCommentRequest
from contracts.comments.get_comments_request import GetCommentsByPostIdRequest
from core.application.usecases.comments.create_comment import CreateComment
from core.application.usecases.comments.delete_comment import DeleteComment
from core.application.usecases.comments.get_comment import (
    GetCommentById,
    GetCommentListByPostId,
)
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from external.web_api.dependencies.authentication import authentication_required
from fastapi import APIRouter, Depends

comment_router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
    route_class=DishkaRoute,
)


@comment_router.post(
    "/",
    status_code=201,
    response_model=CommentDetailsResponse,
    dependencies=[Depends(authentication_required)],
)
async def create_comment(
    create_comment_request: CreateCommentRequest,
    create_comment_interactor: FromDishka[CreateComment],
) -> CommentDetailsResponse:
    return await create_comment_interactor(create_comment_request)


@comment_router.get("/", response_model=CommentListResponse)
async def get_comment_list_by_post_id(
    get_comment_list_request: Annotated[GetCommentsByPostIdRequest, Depends()],
    get_comment_list_interactor: FromDishka[GetCommentListByPostId],
) -> CommentListResponse:
    return await get_comment_list_interactor(get_comment_list_request)


@comment_router.get("/{comment_id}", response_model=CommentDetailsResponse)
async def get_comment_by_id(
    comment_id: UUID,
    get_comment_interactor: FromDishka[GetCommentById],
) -> CommentDetailsResponse:
    return await get_comment_interactor(comment_id)


@comment_router.delete(
    "/{comment_id}",
    status_code=204,
    dependencies=[Depends(authentication_required)],
)
async def delete_comment(
    comment_id: UUID,
    delete_comment_interactor: FromDishka[DeleteComment],
) -> None:
    await delete_comment_interactor(comment_id)
