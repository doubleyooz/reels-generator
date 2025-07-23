import uuid
from typing import Optional
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID  # Use this for PostgreSQL; adjust for other databases
from sqlalchemy.orm import relationship, Mapped, mapped_column
from pydantic import BaseModel
from src.db.database import Base

# Pydantic models for input validation
class UserCreateModel(BaseModel):
    name: str
    email: str

class UserUpdateModel(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: uuid.UUID  # Changed from int to uuid.UUID
    name: str
    email: str

    class Config:
        from_attributes = True

# SQLAlchemy model for database table
class User(Base):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # UUID as primary key
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    reels: Mapped[list["Reel"]] = relationship("Reel", back_populates="user")