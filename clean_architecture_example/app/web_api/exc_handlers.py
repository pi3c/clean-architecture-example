from app.domain.comments.error import CommentAccessDeniedError, CommentNotFoundError
from app.domain.common.error import DomainValidationError
from app.domain.posts.error import PostAccessDeniedError, PostNotFoundError
from app.domain.users.error import (
    UserAlreadyExistsError,
    UserInvalidCredentialsError,
    UserIsNotAuthorizedError,
)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


async def validation_error_exc_handler(request: Request, exc: DomainValidationError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": exc.message})


async def user_authentication_error_exc_handler(request: Request, exc: UserIsNotAuthorizedError) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def user_already_exist_error_exc_handler(request: Request, exc: UserAlreadyExistsError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": exc.message})


async def user_invalid_credentials_error_exc_handler(
    request: Request, exc: UserInvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": exc.message})


async def post_not_found_error_exc_handler(request: Request, exc: PostNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": exc.message})


async def post_access_denied_exc_error_handler(request: Request, exc: PostAccessDeniedError) -> JSONResponse:
    return JSONResponse(status_code=403, content={"detail": exc.message})


async def comment_not_found_error_exc_handler(request: Request, exc: CommentNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": exc.message})


async def comment_access_denied_error_exc_handler(request: Request, exc: CommentAccessDeniedError) -> JSONResponse:
    return JSONResponse(status_code=403, content={"detail": exc.message})


def init_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainValidationError, validation_error_exc_handler)
    app.add_exception_handler(UserIsNotAuthorizedError, user_authentication_error_exc_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exist_error_exc_handler)
    app.add_exception_handler(UserInvalidCredentialsError, user_invalid_credentials_error_exc_handler)
    app.add_exception_handler(PostNotFoundError, post_not_found_error_exc_handler)
    app.add_exception_handler(PostAccessDeniedError, post_access_denied_exc_error_handler)
    app.add_exception_handler(CommentNotFoundError, comment_not_found_error_exc_handler)
    app.add_exception_handler(CommentAccessDeniedError, comment_access_denied_error_exc_handler)
