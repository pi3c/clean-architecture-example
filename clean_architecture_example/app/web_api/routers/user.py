from app.application.contracts.users.current_user_response import CurrentUserResponse
from app.application.usecases.users.get_current_user import GetCurrentUser
from app.web_api.dependencies.authentication import auth_required
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

user_router = APIRouter(
    tags=["Users"],
    prefix="/users",
    route_class=DishkaRoute,
    dependencies=[Depends(auth_required)],
)


@user_router.get("/me", response_model=CurrentUserResponse)
async def current_user(
    current_user_interactor: FromDishka[GetCurrentUser],
) -> CurrentUserResponse:
    return await current_user_interactor()
