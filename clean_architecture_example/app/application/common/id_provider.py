from typing import Protocol

from app.domain.users.user import UserId


class IdProvider(Protocol):
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError
