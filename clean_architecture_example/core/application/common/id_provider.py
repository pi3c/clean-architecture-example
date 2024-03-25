from typing import Protocol

from core.domain.users.user import UserId


class IdProvider(Protocol):
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError
