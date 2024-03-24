from typing import Protocol

from core.domain.users.user import UserId


class JwtTokenProcessor(Protocol):
    def generate_token(self, user_id: UserId) -> str:
        raise NotImplementedError

    def validate_token(self, token: str) -> UserId | None:
        raise NotImplementedError
