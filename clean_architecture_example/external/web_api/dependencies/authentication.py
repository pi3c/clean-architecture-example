from typing import Annotated, cast

from core.application.common.jwt_processor import JwtTokenProcessor
from core.domain.users.error import UserIsNotAuthorizedError
from core.domain.users.repository import UserRepository
from dishka import AsyncContainer
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


async def authentication_required(
    request: Request,
    credentials_provider: Annotated[
        HTTPAuthorizationCredentials,
        Depends(HTTPBearer()),
    ],
) -> None:
    error = UserIsNotAuthorizedError("Invalid authentication credentials provided")

    container = _get_container(request)

    user_repository = await container.get(UserRepository)
    token_processor = await container.get(JwtTokenProcessor)

    user_id = token_processor.validate_token(credentials_provider.credentials)

    if user_id is None:
        raise error

    user = await user_repository.find_by_id(user_id)

    if not user:
        raise error

    request.scope["user"] = user
    request.scope["auth"] = credentials_provider.credentials


def _get_container(request: Request) -> AsyncContainer:
    container_attr = getattr(request.state, "dishka_container")
    return cast(AsyncContainer, container_attr)
