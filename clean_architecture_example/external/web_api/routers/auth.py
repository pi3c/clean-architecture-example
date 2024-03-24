from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from contracts.authentication.authentication_response import AuthenticationResponse
from contracts.authentication.login_request import LoginRequest
from contracts.authentication.register_request import RegisterRequest
from core.application.usecases.authentication.login import Login
from core.application.usecases.authentication.register import Register

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    route_class=DishkaRoute,
)


@auth_router.post("/register", response_model=AuthenticationResponse)
async def register(
    request: RegisterRequest,
    register_interactor: Annotated[Register, FromDishka()],
) -> AuthenticationResponse:
    return await register_interactor(request)


@auth_router.post("/login", response_model=AuthenticationResponse)
async def login(
    request: LoginRequest,
    login_interactor: Annotated[Login, FromDishka()],
) -> AuthenticationResponse:
    return await login_interactor(request)
