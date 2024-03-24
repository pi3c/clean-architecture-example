from typing import Protocol

from core.domain.users.user import User, UserEmail, UserId


class UserRepository(Protocol):
    async def create(self, user: User) -> None:
        raise NotImplementedError

    async def find_by_id(self, id: UserId) -> User | None:
        raise NotImplementedError

    async def find_by_email(self, email: UserEmail) -> User | None:
        raise NotImplementedError
