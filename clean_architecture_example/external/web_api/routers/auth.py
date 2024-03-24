from typing import Annotated

from contracts.authentication.authentication_response import AuthenticationResponse
from contracts.authentication.login_request import LoginRequest
from contracts.authentication.register_request import RegisterRequest
from core.application.usecases.authentication.login import Login
from core.application.usecases.authentication.register import Register
from external.web_api.extensions.rate_limit import limiter

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    route_class=DishkaRoute,
)


@auth_router.post("/register", response_model=AuthenticationResponse)
@limiter.limit("3/minute")
async def register(
    request: Request,
    register_request: RegisterRequest,
    register_interactor: Annotated[Register, FromDishka()],
) -> AuthenticationResponse:
    return await register_interactor(register_request)


@auth_router.post("/login", response_model=AuthenticationResponse)
@limiter.limit("3/minute")
async def login(
    request: Request,
    login_request: LoginRequest,
    login_interactor: Annotated[Login, FromDishka()],
) -> AuthenticationResponse:
    return await login_interactor(login_request)
