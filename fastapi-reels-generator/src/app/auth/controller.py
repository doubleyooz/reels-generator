import jwt
from datetime import timedelta
from fastapi import APIRouter, Depends, Request, status, FastAPI
from typing import List

from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from authlib.oauth2.rfc6749 import OAuth2Token

from src.app.auth.schema import oauth2_scheme
from src.app.auth.exception import AuthBadRequestException, AuthUnauthorisedException
from src.app.auth.schema import AuthResponse
from src.app.auth.service import AuthService
from src.app.users.schema import UserCreateModel
from src.app.users.service import UserService
from src.db.database import Database
from src.env import ACCESS_TOKEN_EXPIRATION, ACCESS_TOKEN_SECRET, ALGORITHM, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
async def get_user_service(request: Request) -> UserService:
    """Dependency to provide ReelService with initialized Database."""
    return UserService(request.app.state.db)


async def get_auth_service(request: Request) -> AuthService:
    """Dependency to provide ReelService with initialized Database."""
    return AuthService()

# New Google OAuth endpoints
@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = GOOGLE_REDIRECT_URI
    print(GOOGLE_REDIRECT_URI)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google", response_model=AuthResponse)
async def auth_google(request: Request, user_service: UserService = Depends(get_user_service), auth_service: AuthService = Depends(get_auth_service)):
    print('hereeee')
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        if not user_info:
            raise AuthBadRequestException()

        # Check if user exists, otherwise create a new one
        email = user_info["email"]
        existing_user = await user_service.find_by_email(email)
        if not existing_user:
            user_data = UserCreateModel(
                name=user_info.get("name", email.split("@")[0]),
                email=email
            )
            print(user_data)
            existing_user = await user_service.create(user_data)

        # Generate JWT token
        access_token = auth_service.create_access_token(data={"sub": email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise AuthBadRequestException(e)
    
async def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)):
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise AuthUnauthorisedException()
        user = await user_service.find_by_email(email)
        if user is None:
            raise AuthUnauthorisedException()
        
        return user     
    except jwt.ExpiredSignatureError:
        raise AuthUnauthorisedException("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthUnauthorisedException("Invalid token")
    except:
            raise AuthUnauthorisedException()

@router.get("/me", response_model=AuthResponse)
async def read_users_me(auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.get_current_user()