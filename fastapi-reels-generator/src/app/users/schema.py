from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel  # For data validation models

Base = declarative_base()

# Pydantic models for input validation
class UserCreateModel(BaseModel):
    name: str
    email: str

class UserUpdateModel(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True  # Enable ORM compatibility to convert SQLAlchemy models

# SQLAlchemy model for database table
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)  # Fixed: Changed Integer to String
    reels: Mapped[list["Reel"]] = relationship("Reel", back_populates="user")