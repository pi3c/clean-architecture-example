from contracts.users.current_user_response import CurrentUserResponse
from core.application.common.interactor import Interactor
from core.application.common.user_context import UserContext


class GetCurrentUser(Interactor[None, CurrentUserResponse]):
    def __init__(self, user_context: UserContext) -> None:
        self.user_context = user_context

    async def __call__(self, request=None) -> CurrentUserResponse:
        user = self.user_context.get_current_user()

        return CurrentUserResponse(
            id=user.id.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            email=user.email.value,
        )
