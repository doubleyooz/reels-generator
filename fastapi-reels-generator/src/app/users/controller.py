import uuid
from fastapi import APIRouter, Depends, Request, status, FastAPI
from typing import List
from sqlalchemy.exc import IntegrityError
from src.db.database import Database
from src.app.users.service import UserService
from src.app.users.schema import UserCreateModel, UserUpdateModel, UserResponse
from src.app.users.exception import UserBadRequestException, UserNotFoundException

async def get_user_service(request: Request) -> UserService:
    """Dependency to provide UserService with initialized Database."""
    return UserService(request.app.state.db)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def find_all(user_service: UserService = Depends(get_user_service)):
    """Retrieve all users."""
    return await user_service.find_all()

'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create(user_data: UserCreateModel, user_service: UserService = Depends(get_user_service)):
    """Create a new user."""
    try:
        return await user_service.create(user_data)
    except IntegrityError:
        raise UserBadRequestException()
'''

@router.get("/{_id}", response_model=UserResponse)
async def find_by_id(_id: uuid.UUID, user_service: UserService = Depends(get_user_service)):
    """Retrieve a user by ID."""
    user = await user_service.find_by_id(_id)
    if user is None:
        raise UserNotFoundException(_id)
    return user

@router.patch("/{_id}", response_model=UserResponse)
async def update(
    _id: uuid.UUID,
    user_update_data: UserUpdateModel,
    user_service: UserService = Depends(get_user_service),
):
    """Update a user by ID."""
    user = await user_service.update(_id, user_update_data)
    if user is None:
        raise UserNotFoundException(_id)
    return user

@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(_id: uuid.UUID, user_service: UserService = Depends(get_user_service)):
    """Delete a user by ID."""
    success = await user_service.delete(_id)
    if not success:
        raise UserNotFoundException(_id)
    return {}