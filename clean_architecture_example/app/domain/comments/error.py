from app.domain.common.error import DomainError


class CommentAccessDeniedError(DomainError):
    pass


class CommentNotFoundError(DomainError):
    pass
