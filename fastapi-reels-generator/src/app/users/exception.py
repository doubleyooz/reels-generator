from fastapi import HTTPException, status

class UserNotFoundException(HTTPException):
    def __init__(self, msg = "User not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=msg)

class UserBadRequestException(HTTPException):
    def __init__(self, msg = "Invalid User data."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)