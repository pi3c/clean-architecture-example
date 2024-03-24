from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticationToken:
    token: str
