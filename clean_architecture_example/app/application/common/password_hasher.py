from typing import Protocol


class PasswordHasher(Protocol):
    @staticmethod
    def hash_password(password: str) -> str:
        raise NotImplementedError

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        raise NotImplementedError
