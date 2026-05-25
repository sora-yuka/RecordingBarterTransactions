from src.config.exceptions import BaseAppException, status


class UserAlreadyExistsException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "User with this identity is already exists"


class InvalidCredentialsException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "Incorrect credentials provided"


class InvalidTokenException(Exception):
    def __init__(self, message: str = "Could not validate provided token"):
        self.message = message
        super().__init__(self.message)


class TokenExpiredException(InvalidTokenException):
    def __init__(self, message: str = "Token has expired"):
        self.message = message
        super().__init__(self.message)
