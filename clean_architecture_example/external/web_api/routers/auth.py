from contracts.authentication.authentication_response import AuthenticationResponse
from contracts.authentication.login_request import LoginRequest
from contracts.authentication.register_request import RegisterRequest
from core.application.usecases.authentication.login import Login
from core.application.usecases.authentication.register import Register

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    route_class=DishkaRoute,
)


@auth_router.post("/register", response_model=AuthenticationResponse)
async def register(
    register_request: RegisterRequest,
    register_interactor: FromDishka[Register],
) -> AuthenticationResponse:
    return await register_interactor(register_request)


@auth_router.post("/login", response_model=AuthenticationResponse)
async def login(
    login_request: LoginRequest,
    login_interactor: FromDishka[Login],
) -> AuthenticationResponse:
    return await login_interactor(login_request)
