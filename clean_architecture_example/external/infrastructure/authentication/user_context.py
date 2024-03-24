from fastapi import Request

from core.application.common.user_context import UserContext
from core.domain.users.user import User


class FastAPIUserContext(UserContext):
    def __init__(self, request: Request) -> None:
        self.request = request

    def get_current_user(self) -> User:
        return self.request.user
