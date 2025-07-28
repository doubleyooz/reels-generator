import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.database import Database
from src.db.repository import Repository
from src.app.users.schema import UserCreateModel, UserResponse, UserUpdateModel, User

class UserService:
    def __init__(self, db: Database):
        """
        Initialize the UserService with a Database instance.
        
        Args:
            db: The Database instance for session management.
        """
        self.repository = Repository(User, db)

    async def find_all(self) -> List[User]:
        """
        Retrieve all users from the database.
        
        Returns:
            A list of User objects.
        """
        users = await self.repository.find_all()
        return [User.from_orm(user) for user in users]


    async def create(self, data: UserCreateModel) -> UserResponse:
        """
        Create a new user in the database.
        
        Args:
            data: The data for the new user.
        
        Returns:
            The created User object.
        """
        user_dict = data.dict(exclude_unset=True)
    
        return await self.repository.create(**user_dict)
       
    
    async def find_by_id(self, _id: uuid.UUID) -> Optional[User]:
        """
        Retrieve a user by its ID.
        
        Args:
            _id: The ID of the user to retrieve.
        
        Returns:
            The User object if found, else None.
        """
        return await self.repository.find_by_id(_id)

    async def find_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by its ID.
        
        Args:
            _id: The ID of the user to retrieve.
        
        Returns:
            The User object if found, else None.
        """
        return await self.repository.find_one( {"email": email} )

    async def update(self, _id: uuid.UUID, user_update_data: UserUpdateModel) -> Optional[User]:
        """
        Update a user by its ID.
        
        Args:
            _id: The ID of the user to update.
            user_update_data: The data to update the user with.
        
        Returns:
            The updated User object if found, else None.
        """
        return await self.repository.update(_id, **user_update_data.dict(exclude_unset=True))

    async def delete(self, user_id: uuid.UUID) -> bool:
        """
        Delete a user by its ID.
        
        Args:
            user_id: The ID of the user to delete.
        
        Returns:
            True if the user was deleted, False if not found.
        """
        return await self.repository.delete(user_id)