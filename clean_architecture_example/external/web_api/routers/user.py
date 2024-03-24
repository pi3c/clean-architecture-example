from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from contracts.users.current_user_response import CurrentUserResponse
from core.application.usecases.users.get_current_user import GetCurrentUser
from external.web_api.authentication.jwt_auth import authentication_required

user_router = APIRouter(
    tags=["Users"],
    prefix="/users",
    route_class=DishkaRoute,
    dependencies=[Depends(authentication_required)],
)


@user_router.get("/me", response_model=CurrentUserResponse)
async def current_user(
    current_user_interactor: Annotated[GetCurrentUser, FromDishka()],
) -> CurrentUserResponse:
    return await current_user_interactor()
