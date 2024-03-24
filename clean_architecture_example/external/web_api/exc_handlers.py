from typing import Awaitable, Callable, Type

from fastapi import Request
from fastapi.responses import JSONResponse

from core.domain.common.error import DomainError, DomainValidationError
from core.domain.posts.error import PostNotFoundError
from core.domain.users.error import (
    UserAlreadyExistsError,
    UserInvalidCredentialsError,
    UserIsNotAuthorizedError,
)


async def validation_error_exc_handler(
    request: Request, exc: DomainValidationError
) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": exc.message})


async def user_authentication_error_exc_handler(
    request: Request, exc: UserIsNotAuthorizedError
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def user_already_exist_error_exc_handler(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": exc.message})


async def user_invalid_credentials_error_exc_handler(
    request: Request, exc: UserInvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": exc.message})


async def post_not_found_exc_handler(
    request: Request, exc: PostNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": exc.message})


ExceptionHandlerType = Callable[[Request, DomainError], Awaitable[JSONResponse]]

HANDLERS: dict[Type[DomainError], ExceptionHandlerType] = {
    DomainValidationError: validation_error_exc_handler,
    UserIsNotAuthorizedError: user_authentication_error_exc_handler,
    UserAlreadyExistsError: user_already_exist_error_exc_handler,
    UserInvalidCredentialsError: user_invalid_credentials_error_exc_handler,
    PostNotFoundError: post_not_found_exc_handler,
}
