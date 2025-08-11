import jwt
from datetime import datetime, timedelta, timezone

from src.auth.exception import AuthUnauthorisedException
from src.env import ACCESS_TOKEN_EXPIRATION, ACCESS_TOKEN_SECRET, ALGORITHM 

def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise AuthUnauthorisedException("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthUnauthorisedException("Invalid token")
    except:
        raise AuthUnauthorisedException()
    
def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRATION))
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
    return encoded_jwt