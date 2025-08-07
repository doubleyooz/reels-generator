from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from src.db.database import Database
from src.auth.service import AuthService
from src.models.reels.service import ReelService
from src.models.users.service import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_database(request: Request) -> Database:
    """Provide the Database instance from app state."""
    return request.app.state.db

async def get_auth_service(db: Database = Depends(get_database)) -> AuthService:
    """Dependency to provide ReelService with initialized Database."""
    return AuthService(UserService(db))

async def get_reel_service(db: Database = Depends(get_database)) -> ReelService:
    """Provide ReelService with initialized Database."""
    return ReelService(db)

async def get_user_service(db: Database = Depends(get_database)) -> UserService:
    """Provide UserService with initialized Database."""
    return UserService(db)


