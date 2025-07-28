import uuid
from typing import Annotated, List, Optional
from pydantic import BaseModel
from sqlalchemy import String, ForeignKey, DateTime, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID  # For PostgreSQL UUID support
from src.db.database import Base
from src.env import DB_CONNECTION
from datetime import datetime

class ReelResponse(BaseModel):
    id: uuid.UUID  # Changed from int to uuid.UUID
    title: str
    file: str
    user_id: uuid.UUID  # Changed from int to uuid.UUID
    created_at: datetime = None

    class Config:
        from_attributes = True

class Reel(Base):
    __tablename__ = 'reels'
    title = Column(String, nullable=False)
    file = Column(String, nullable=False)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True
    )  # Changed to UUID for ForeignKey
    user: Mapped["User"] = relationship(back_populates="reels")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class ReelCreateModel(BaseModel):
    title: str
    file: str
    user_id: uuid.UUID  # Changed from int to uuid.UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReelGenerateModel(BaseModel):
    title: str
    audio: str
    images: List[str]
    user_id: uuid.UUID  # Changed from int to uuid.UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReelUpdateModel(BaseModel):
    title: Optional[str] = None
    file: Optional[str] = None

    class Config:
        from_attributes = True