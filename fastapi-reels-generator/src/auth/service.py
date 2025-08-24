import jwt
from datetime import datetime, timedelta, timezone

from src.auth.exception import AuthUnauthorisedException
from src.env import ACCESS_TOKEN_EXPIRATION, ACCESS_TOKEN_SECRET, ALGORITHM
from src.models.users.service import UserService
from src.models.users.schema import UserCreateModel

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        
    def create_access_token(self, data: dict):
        print('create access token')
        to_encode = data.copy()
        expires_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRATION))
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

    async def login_google(self, data: UserCreateModel):
        email = data.email
        name = data.name
        
        existing_user = await self.user_service.find_by_email(email)
        if not existing_user:
            print('creating new user')
            user_data = UserCreateModel(
                name=name,
                email=email
            )
            print(user_data)
            existing_user = await self.user_service.create(user_data)
        return existing_user 
            
   