from typing import Protocol

from core.domain.posts.post import Post, PostId
from core.domain.users.user import UserId


class PostRepository(Protocol):
    async def create(self, post: Post) -> None:
        raise NotImplementedError

    async def find_all(self, limit: int = 20, offset: int = 0) -> list[Post] | None:
        raise NotImplementedError

    async def find_by_id(self, id: PostId) -> Post | None:
        raise NotImplementedError

    async def find_by_owner_id(
        self, owner_id: UserId, limit: int = 20, offset: int = 0
    ) -> list[Post] | None:
        raise NotImplementedError
