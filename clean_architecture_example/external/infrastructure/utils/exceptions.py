class MissingEnvVariableError(Exception):
    def __init__(self, var_name: str, *args: object) -> None:
        message = f"Variable {var_name} is not set"
        super().__init__(message, *args)
