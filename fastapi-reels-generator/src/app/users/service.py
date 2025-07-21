from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.database import Database
from src.db.repository import Repository
from src.app.users.schema import UserCreateModel, UserUpdateModel, User

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


    async def create(self, data: UserCreateModel) -> User:
        """
        Create a new user in the database.
        
        Args:
            data: The data for the new user.
        
        Returns:
            The created User object.
        """
        user_dict = data.dict(exclude_unset=True)
    
        user = await self.repository.create(**user_dict)
        return User.from_orm(user)

    async def find_by_id(self, _id: int) -> Optional[User]:
        """
        Retrieve a user by its ID.
        
        Args:
            _id: The ID of the user to retrieve.
        
        Returns:
            The User object if found, else None.
        """
        user = await self.repository.find_by_id(_id)
        return User.from_orm(user) if user else None

    async def update(self, _id: int, user_update_data: UserUpdateModel) -> Optional[User]:
        """
        Update a user by its ID.
        
        Args:
            _id: The ID of the user to update.
            user_update_data: The data to update the user with.
        
        Returns:
            The updated User object if found, else None.
        """
        user = await self.repository.update(_id, **user_update_data.dict(exclude_unset=True))
        return User.from_orm(user) if user else None

    async def delete(self, user_id: int) -> bool:
        """
        Delete a user by its ID.
        
        Args:
            user_id: The ID of the user to delete.
        
        Returns:
            True if the user was deleted, False if not found.
        """
        return await self.repository.delete(user_id)