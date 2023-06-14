from fastapi import HTTPException, status


class InvalidUsernameException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username",
        )
