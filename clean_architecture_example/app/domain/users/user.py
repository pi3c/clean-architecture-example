import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from app.domain.common.entity import Entity
from app.domain.common.error import DomainValidationError
from app.domain.common.value_object import ValueObject


@dataclass(frozen=True)
class UserEmail(ValueObject):
    value: str

    def __post_init__(self) -> None:
        pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, self.value):
            raise DomainValidationError(
                "Invalid email format. Email must be in the format 'example@example.com'."
            )


@dataclass(frozen=True)
class UserFirstName(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if len(self.value) < 1:
            raise DomainValidationError("First name must be at least 1 character long.")
        if len(self.value) > 100:
            raise DomainValidationError(
                "First name must be at most 100 characters long."
            )
        if not self.value.isalpha():
            raise DomainValidationError("First name must only contain letters.")


@dataclass(frozen=True)
class UserLastName(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if len(self.value) < 1:
            raise DomainValidationError("Last name must be at least 1 character long.")
        if len(self.value) > 100:
            raise DomainValidationError(
                "Last name must be at most 100 characters long."
            )
        if not self.value.isalpha():
            raise DomainValidationError("Last name must only contain letters.")


@dataclass(frozen=True)
class UserId(ValueObject):
    value: UUID


@dataclass
class User(Entity[UserId]):
    first_name: UserFirstName
    last_name: UserLastName
    email: UserEmail
    hashed_password: str

    @staticmethod
    def create(
        first_name: str, last_name: str, email: str, hashed_password: str
    ) -> "User":
        return User(
            id=UserId(uuid4()),
            email=UserEmail(email),
            hashed_password=hashed_password,
            last_name=UserLastName(last_name),
            first_name=UserFirstName(first_name),
        )
