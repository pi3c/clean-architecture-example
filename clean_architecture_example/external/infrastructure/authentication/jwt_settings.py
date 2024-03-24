from dataclasses import dataclass, field


@dataclass(frozen=True)
class JwtSettings:
    secret: str
    expires_in: int = field(default=2)
    algorithm: str = field(default="HS256")
