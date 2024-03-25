from core.application.common.id_provider import IdProvider
from core.application.common.jwt_processor import JwtTokenProcessor
from core.domain.users.error import UserIsNotAuthorizedError
from core.domain.users.user import UserId


class JwtTokenIdProvider(IdProvider):
    def __init__(self, token_processor: JwtTokenProcessor, token: str) -> None:
        self.token_processor = token_processor
        self.token = token

    def get_current_user_id(self) -> UserId:
        user_id = self.token_processor.validate_token(self.token)

        if user_id is None:
            raise UserIsNotAuthorizedError("Invalid authorization credentials provided")

        return user_id
