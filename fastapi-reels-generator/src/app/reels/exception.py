from fastapi import HTTPException, status

class ReelNotFoundException(HTTPException):
    def __init__(self, msg = "Reel not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=msg)

class ReelBadRequestException(HTTPException):
    def __init__(self, msg = "Invalid reel data."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)