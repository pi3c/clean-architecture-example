from dataclasses import dataclass

from app.infrastructure.authentication.jwt_settings import JwtSettings
from app.infrastructure.persistence.db_settings import DatabaseSettings


@dataclass(frozen=True)
class MainSettings:
    jwt_settings: JwtSettings
    db_settings: DatabaseSettings
