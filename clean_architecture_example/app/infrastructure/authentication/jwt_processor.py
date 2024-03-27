from datetime import timedelta
from uuid import UUID

from app.application.common.date_time_provider import DateTimeProvider
from app.application.common.jwt_processor import JwtTokenProcessor
from app.domain.users.user import UserId
from app.infrastructure.authentication.jwt_settings import JwtSettings
from jose import JWTError
from jose.jwt import decode, encode


class JoseJwtTokenProcessor(JwtTokenProcessor):
    def __init__(
        self, jwt_options: JwtSettings, date_time_provider: DateTimeProvider
    ) -> None:
        self.jwt_options = jwt_options
        self.date_time_provider = date_time_provider

    def generate_token(self, user_id: UserId) -> str:
        issued_at = self.date_time_provider.get_current_time()
        expiration_time = issued_at + timedelta(hours=self.jwt_options.expires_in)

        claims = {
            "iat": issued_at,
            "exp": expiration_time,
            "sub": str(user_id.value),
        }

        return encode(claims, self.jwt_options.secret, self.jwt_options.algorithm)

    def validate_token(self, token: str) -> UserId | None:
        try:
            payload = decode(
                token, self.jwt_options.secret, [self.jwt_options.algorithm]
            )

            return UserId(UUID(payload["sub"]))

        except (JWTError, ValueError, KeyError):
            return None
