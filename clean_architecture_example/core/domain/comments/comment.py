from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from core.domain.common.entity import Entity
from core.domain.common.error import DomainValidationError
from core.domain.common.value_object import ValueObject
from core.domain.posts.post import PostId
from core.domain.users.user import UserId


@dataclass(frozen=True)
class CommentId(ValueObject):
    value: UUID


@dataclass(frozen=True)
class CommentContent(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise DomainValidationError("Comment content cannot be empty")

        if len(self.value) > 1000:
            raise DomainValidationError(
                "Invalid comment content. Comment content must be less than 1000 characters."
            )


@dataclass
class Comment(Entity[CommentId]):
    content: CommentContent
    post_id: PostId
    owner_id: UserId
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        content: str,
        post_id: UUID,
        owner_id: UUID,
        created_at: datetime,
        updated_at: datetime,
    ) -> "Comment":
        return Comment(
            id=CommentId(value=uuid4()),
            content=CommentContent(value=content),
            post_id=PostId(value=post_id),
            owner_id=UserId(value=owner_id),
            created_at=created_at,
            updated_at=updated_at,
        )
