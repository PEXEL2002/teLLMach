from fastapi import HTTPException, status


class APIException(HTTPException):
    """Base API exception"""

    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundException(APIException):
    def __init__(self):
        super().__init__(
            detail="User not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UserAlreadyExistsException(APIException):
    def __init__(self):
        super().__init__(
            detail="Email already registered",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class InvalidCredentialsException(APIException):
    def __init__(self):
        super().__init__(
            detail="Invalid credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
