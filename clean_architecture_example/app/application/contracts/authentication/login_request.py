from dataclasses import dataclass


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str
