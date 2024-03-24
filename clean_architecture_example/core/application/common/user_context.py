from typing import Protocol

from core.domain.users.user import User


class UserContext(Protocol):
    def get_current_user(self) -> User:
        raise NotImplementedError
