from app.application.common.interactor import Interactor
from app.application.common.password_hasher import PasswordHasher
from app.application.contracts.authentication.authentication_response import (
    AuthenticationResponse,
)
from app.application.contracts.authentication.login_request import LoginRequest
from app.domain.users.error import UserInvalidCredentialsError
from app.domain.users.repository import UserRepository
from app.domain.users.user import UserEmail


class Login(Interactor[LoginRequest, AuthenticationResponse]):
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def __call__(self, request: LoginRequest) -> AuthenticationResponse:
        user = await self.user_repository.find_by_email(
            UserEmail(
                request.email,
            )
        )
        error = UserInvalidCredentialsError("Email or password is incorrect")
        if user is None:
            raise error

        if not self.password_hasher.verify_password(request.password, user.hashed_password):
            raise error

        return AuthenticationResponse(
            id=user.id.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            email=user.email.value,
        )
