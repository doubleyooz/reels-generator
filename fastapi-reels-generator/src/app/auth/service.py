import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends

from src.app.auth.exception import AuthUnauthorisedException
from src.env import ACCESS_TOKEN_EXPIRATION, ACCESS_TOKEN_SECRET, ALGORITHM

class AuthService:
    def create_access_token(data: dict):
        to_encode = data.copy()
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

   