from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.exception import AuthUnauthorisedException
from src.common.jwt_handler import decode_jwt


class JWTGuard(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTGuard, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTGuard, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthUnauthorisedException("Invalid authentication scheme.")
            payload = self.verify_jwt(credentials.credentials)
            if payload is None:
                raise AuthUnauthorisedException("Invalid token or expired token.")
            print('Verified token:', payload)
            return payload
        else:
            raise AuthUnauthorisedException("Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        
        return payload