import uuid
from typing import Type, TypeVar, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.database import Database
from src.models.users.schema import User
from src.models.reels.schema import Reel

# Define a generic type for models
T = TypeVar('T')

class Repository:
    def __init__(self, model: Type[T], db: Database):
        """
        Initialize the repository with a specific model and Database instance.
        
        Args:
            model: The SQLAlchemy model class (e.g., User, Reel).
            db: The Database instance for session management.
        """
        self.model = model
        self.db = db

    async def create(self, **attributes) -> T:
        """
        Create a new record in the database, generating a UUID for the 'id' if not provided.
        
        Args:
            **attributes: Attributes to set on the new model instance.
        
        Returns:
            The created model instance.
        """
        async with await self.db.get_session() as session:
            # Generate a UUID if 'id' is not provided in attributes
            if 'id' not in attributes:
                attributes['id'] = uuid.uuid4()
            instance = self.model(**attributes)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def find_by_id(self, id: uuid.UUID) -> Optional[T]:
        """
        Find a record by its UUID.
        
        Args:
            id: The UUID of the record to find.
        
        Returns:
            The model instance if found, else None.
        """
        async with await self.db.get_session() as session:
            result = await session.execute(select(self.model).filter(self.model.id == id))
            return result.scalars().first()

    async def find_one(self, data: dict) -> Optional[T]:
        """
        Find a single record matching the provided attributes.
        
        Args:
            data: A dictionary of attribute names and values to filter by (e.g., {"email": "user@example.com"}).
        
        Returns:
            The model instance if found, else None.
        """
        print(data)
        async with await self.db.get_session() as session:
            query = select(self.model)
            for key, value in data.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
                else:
                    raise ValueError(f"Invalid attribute {key} for model {self.model.__name__}")
            result = await session.execute(query)
            return result.scalars().first()

    async def find_all(self) -> List[T]:
        """
        Retrieve all records for the model.
        
        Returns:
            A list of all model instances.
        """
        async with await self.db.get_session() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def update(self, id: uuid.UUID, **attributes) -> Optional[T]:
        """
        Update a record by its UUID.
        
        Args:
            id: The UUID of the record to update.
            **attributes: Attributes to update on the model instance.
        
        Returns:
            The updated model instance if found, else None.
        """
        async with await self.db.get_session() as session:
            result = await session.execute(select(self.model).filter(self.model.id == id))
            instance = result.scalars().first()
            if instance:
                for key, value in attributes.items():
                    setattr(instance, key, value)
                await session.commit()
                await session.refresh(instance)
                return instance
            return None

    async def delete(self, id: uuid.UUID) -> bool:
        """
        Delete a record by its UUID.
        
        Args:
            id: The UUID of the record to delete.
        
        Returns:
            True if the record was deleted, False if not found.
        """
        async with await self.db.get_session() as session:
            result = await session.execute(select(self.model).filter(self.model.id == id))
            instance = result.scalars().first()
            if instance:
                await session.delete(instance)
                await session.commit()
                return True
            return False