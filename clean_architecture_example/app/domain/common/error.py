class DomainError(Exception):
    """Base error for all domain errors"""

    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)


class DomainValidationError(DomainError):
    pass
