from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.database import Database
from src.db.repository import Repository
from src.app.reels.schema import ReelCreateModel, ReelUpdateModel, Reel

class ReelService:
    def __init__(self, db: Database):
        """
        Initialize the ReelService with a Database instance.
        
        Args:
            db: The Database instance for session management.
        """
        self.repository = Repository(Reel, db)

    async def find_all(self) -> List[Reel]:
        """
        Retrieve all reels from the database.
        
        Returns:
            A list of Reel objects.
        """
        reels = await self.repository.find_all()
        return [Reel.from_orm(reel) for reel in reels]

    async def find_by_user(self, user_id: int) -> List[Reel]:
        """
        Retrieve all reels for a specific user.
        
        Args:
            user_id: The ID of the user whose reels to retrieve.
        
        Returns:
            A list of Reel objects for the user.
        """
        async with self.repository.db.get_session() as session:
            result = await session.execute(select(Reel).filter(Reel.user_id == user_id))
            reels = result.scalars().all()
            return [Reel.from_orm(reel) for reel in reels]

    async def create(self, reel_data: ReelCreateModel) -> Reel:
        """
        Create a new reel in the database.
        
        Args:
            reel_data: The data for the new reel.
        
        Returns:
            The created Reel object.
        """
        reel_dict = reel_data.dict(exclude_unset=True)
        if not reel_dict.get('created_at'):
            del reel_dict['created_at']  # Let model default handle created_at
        reel = await self.repository.create(**reel_dict)
        return Reel.from_orm(reel)

    async def find_by_id(self, reel_id: int) -> Optional[Reel]:
        """
        Retrieve a reel by its ID.
        
        Args:
            reel_id: The ID of the reel to retrieve.
        
        Returns:
            The Reel object if found, else None.
        """
        reel = await self.repository.find_by_id(reel_id)
        return Reel.from_orm(reel) if reel else None

    async def update(self, reel_id: int, reel_update_data: ReelUpdateModel) -> Optional[Reel]:
        """
        Update a reel by its ID.
        
        Args:
            reel_id: The ID of the reel to update.
            reel_update_data: The data to update the reel with.
        
        Returns:
            The updated Reel object if found, else None.
        """
        reel = await self.repository.update(reel_id, **reel_update_data.dict(exclude_unset=True))
        return Reel.from_orm(reel) if reel else None

    async def delete(self, reel_id: int) -> bool:
        """
        Delete a reel by its ID.
        
        Args:
            reel_id: The ID of the reel to delete.
        
        Returns:
            True if the reel was deleted, False if not found.
        """
        return await self.repository.delete(reel_id)