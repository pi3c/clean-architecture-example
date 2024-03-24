from dataclasses import dataclass

from external.infrastructure.authentication.jwt_settings import JwtSettings
from external.infrastructure.persistence.db_settings import DatabaseSettings


@dataclass(frozen=True)
class MainSettings:
    jwt_settings: JwtSettings
    db_settings: DatabaseSettings
