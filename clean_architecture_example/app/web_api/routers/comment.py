from typing import Annotated
from uuid import UUID

from app.application.contracts.comments.comment_details_response import (
    CommentDetailsResponse,
)
from app.application.contracts.comments.comment_list_response import CommentListResponse
from app.application.contracts.comments.create_comment_request import (
    CreateCommentRequest,
)
from app.application.contracts.comments.get_comments_request import (
    GetCommentsByPostIdRequest,
)
from app.application.contracts.comments.update_comment import UpdateCommentRequest
from app.application.usecases.comments.create_comment import CreateComment
from app.application.usecases.comments.delete_comment import DeleteComment
from app.application.usecases.comments.get_comment import (
    GetCommentById,
    GetCommentListByPostId,
)
from app.application.usecases.comments.update_comment import UpdateComment
from app.web_api.dependencies.authentication import auth_required
from app.web_api.schemas.comment import UpdateCommentSchema
from dishka.integrations.fastapi import DishkaRoute, FromDishka
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
    dependencies=[Depends(auth_required)],
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


@comment_router.patch(
    "/{comment_id}",
    dependencies=[Depends(auth_required)],
    response_model=CommentDetailsResponse,
)
async def update_comment(
    comment_id: UUID,
    update_comment_request: UpdateCommentSchema,
    update_comment_interactor: FromDishka[UpdateComment],
) -> CommentDetailsResponse:
    return await update_comment_interactor(
        UpdateCommentRequest(
            comment_id,
            update_comment_request.content,
        ),
    )


@comment_router.delete(
    "/{comment_id}",
    status_code=204,
    dependencies=[Depends(auth_required)],
)
async def delete_comment(
    comment_id: UUID,
    delete_comment_interactor: FromDishka[DeleteComment],
) -> None:
    await delete_comment_interactor(comment_id)
