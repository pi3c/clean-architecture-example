from app.application.common.interactor import Interactor
from app.application.common.password_hasher import PasswordHasher
from app.application.common.unit_of_work import UnitOfWork
from app.application.contracts.authentication.authentication_response import (
    AuthenticationResponse,
)
from app.application.contracts.authentication.register_request import RegisterRequest
from app.domain.users.error import UserAlreadyExistsError
from app.domain.users.repository import UserRepository
from app.domain.users.user import User, UserEmail


class Register(Interactor[RegisterRequest, AuthenticationResponse]):
    def __init__(
        self,
        uow: UnitOfWork,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self.uow = uow
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def __call__(self, request: RegisterRequest) -> AuthenticationResponse:
        user_exists = await self.user_repository.find_by_email(UserEmail(request.email))

        if user_exists:
            raise UserAlreadyExistsError("User with that email already exists")

        user = User.create(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            hashed_password=self.password_hasher.hash_password(request.password),
        )

        await self.user_repository.create(user)
        await self.uow.commit()

        return AuthenticationResponse(
            id=user.id.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            email=user.email.value,
        )
