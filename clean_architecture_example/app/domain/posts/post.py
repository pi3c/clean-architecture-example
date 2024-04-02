from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.common.entity import Entity
from app.domain.common.error import DomainValidationError
from app.domain.common.value_object import ValueObject
from app.domain.users.user import UserId


@dataclass(frozen=True)
class PostId(ValueObject):
    value: UUID


@dataclass(frozen=True)
class PostTitle(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise DomainValidationError("Post title is required.")

        if len(self.value) > 100:
            raise DomainValidationError("Invalid post title. Post title must be less than 100 characters.")


@dataclass(frozen=True)
class PostContent(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise DomainValidationError("Post content is required.")

        if len(self.value) > 1000:
            raise DomainValidationError("Invalid post content. Post content must be less than 1000 characters.")


@dataclass
class Post(Entity):
    id: PostId
    title: PostTitle
    owner_id: UserId
    content: PostContent
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        title: str,
        content: str,
        owner_id: UserId,
        created_at: datetime,
        updated_at: datetime,
    ) -> "Post":
        return Post(
            owner_id=owner_id,
            id=PostId(value=uuid4()),
            title=PostTitle(value=title),
            content=PostContent(value=content),
            created_at=created_at,
            updated_at=updated_at,
        )
