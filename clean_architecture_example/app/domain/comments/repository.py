from datetime import datetime
from typing import Protocol

from app.domain.comments.comment import Comment, CommentContent, CommentId
from app.domain.posts.post import PostId


class CommentRepository(Protocol):
    async def create(self, comment: Comment) -> None:
        raise NotImplementedError

    async def update(self, id: CommentId, content: CommentContent, updated_at: datetime) -> None:
        raise NotImplementedError

    async def find_by_id(self, id: CommentId) -> Comment | None:
        raise NotImplementedError

    async def find_by_post_id(self, post_id: PostId, limit: int = 20, offset: int = 0) -> list[Comment] | None:
        raise NotImplementedError

    async def delete(self, id: CommentId) -> None:
        raise NotImplementedError
