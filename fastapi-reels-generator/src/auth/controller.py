
from datetime import timedelta
from fastapi import APIRouter, Depends, Request, status, FastAPI, HTTPException

from authlib.integrations.starlette_client import OAuth


from src.auth.schema import oauth2_scheme
from src.auth.exception import AuthBadRequestException, AuthUnauthorisedException
from src.auth.schema import AuthResponse
from src.auth.service import AuthService

from src.models.users.schema import UserCreateModel
from src.models.users.service import UserService
from src.db.database import Database
from src.common.jwt_handler import decode_jwt
from src.env import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
from src.dependencies import get_user_service, get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# New Google OAuth endpoints
@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = GOOGLE_REDIRECT_URI
    print(GOOGLE_REDIRECT_URI)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google", response_model=AuthResponse)
async def auth_google(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    print('hereeee')
    try:
        token = await oauth.google.authorize_access_token(request)
       
        user_info = token.get("userinfo")
        email = user_info["email"]
        if not user_info:
            print('No user info')
            raise AuthBadRequestException()

        # Check if user exists, otherwise create a new one
        print('Check if user exists, otherwise create a new one')
        user = await auth_service.login_google(UserCreateModel(email=email, name=user_info.get("name", email.split("@")[0])))
        print('user', user)
        # Generate JWT token
        print('Generate JWT token')
        access_token = auth_service.create_access_token(data={"sub": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise AuthBadRequestException(e)
    
async def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)):
    
    try:
        payload = decode_jwt(token)
        id: str = payload.get("sub")
        if id is None:
            raise AuthUnauthorisedException()
        user = await user_service.find_by_id(id)
        if user is None:
            raise AuthUnauthorisedException()
        
        return user
    except:
        raise AuthUnauthorisedException()    
  

@router.get("/me", response_model=AuthResponse)
async def read_users_me(auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.get_current_user()