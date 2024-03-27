from typing import Annotated
from app.application.common.jwt_processor import JwtTokenProcessor
from app.domain.users.user import UserId
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Response

from app.application.contracts.authentication.authentication_response import (
    AuthenticationResponse,
)
from app.application.contracts.authentication.login_request import LoginRequest
from app.application.contracts.authentication.register_request import RegisterRequest
from app.application.usecases.authentication.login import Login
from app.application.usecases.authentication.register import Register
from fastapi.security import OAuth2PasswordRequestForm

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
    response: Response,
    login_request: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_interactor: FromDishka[Login],
    token_processor: FromDishka[JwtTokenProcessor],
) -> AuthenticationResponse:
    user = await login_interactor(
        LoginRequest(
            email=login_request.username,
            password=login_request.password,
        )
    )
    token = token_processor.generate_token(UserId(user.id))
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)

    return user
