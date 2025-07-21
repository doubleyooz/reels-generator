from fastapi import HTTPException, status

class AuthBadRequestException(HTTPException):
    def __init__(self, msg: str = "Invalid auth data."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

class AuthUnauthorisedException(HTTPException):
    def __init__(self, msg: str = "Unauthorised request."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)