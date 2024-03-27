from app.domain.common.error import DomainError


class PostNotFoundError(DomainError):
    pass


class PostAccessDeniedError(DomainError):
    pass
