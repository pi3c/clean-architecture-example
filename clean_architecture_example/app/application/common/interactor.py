from typing import Generic, Protocol, TypeVar

Request = TypeVar("Request")
Response = TypeVar("Response")


class Interactor(Generic[Request, Response], Protocol):
    async def __call__(self, request: Request) -> Response:
        raise NotImplementedError
