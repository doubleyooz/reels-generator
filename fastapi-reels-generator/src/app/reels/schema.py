from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, String, Integer, ForeignKey, DateTime, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.database import Base
from src.env import DB_CONNECTION
from datetime import datetime

class ReelResponse(BaseModel):
    id: int
    file: str
    audio: str
    images: List[str]
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True  # Enable ORM compatibility to convert SQLAlchemy models

class Reel(Base):
    __tablename__ = 'reels'

    file = Column(String, nullable=False)
    audio = Column(String, nullable=False)
    images = Column(ARRAY(String), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="reels")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
class ReelCreateModel(BaseModel):
    file: str
    audio: str
    images: List[str]
    user_id: int
    created_at: datetime = None  # Optional, will use default in model if not provided

    class Config:
        from_attributes = True

class ReelUpdateModel(BaseModel):
    file: str | None = None
    audio: str | None = None
    images: List[str] | None = None

    class Config:
        from_attributes = True
