from contracts.users.current_user_response import CurrentUserResponse
from core.application.common.interactor import Interactor
from core.application.common.id_provider import IdProvider
from core.domain.users.error import UserIsNotAuthorizedError
from core.domain.users.repository import UserRepository


class GetCurrentUser(Interactor[None, CurrentUserResponse]):
    def __init__(
        self, id_provider: IdProvider, user_repository: UserRepository
    ) -> None:
        self.id_provider = id_provider
        self.user_repository = user_repository

    async def __call__(self, request=None) -> CurrentUserResponse:
        user_id = self.id_provider.get_current_user_id()

        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise UserIsNotAuthorizedError("Invalid authorization credentials provided")

        return CurrentUserResponse(
            id=user.id.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            email=user.email.value,
        )
