from core.domain.common.error import DomainError


class UserInvalidCredentialsError(DomainError):
    pass


class UserAlreadyExistsError(DomainError):
    pass


class UserIsNotAuthorizedError(DomainError):
    pass
