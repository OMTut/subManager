from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for the users table.
    
    Attributes:
        userID: Primary key
        userName: User name
    """
    __tablename__ = "users"
    
    userID = Column(Integer, primary_key=True, index=True)
    userName = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<User {self.userName}>"


# Pydantic models for API request/response validation
class UserBase(BaseModel):
    """Base Pydantic model for user data"""
    userName: str = Field(..., example="Acme Inc.", description="Name of the user")


class UserCreate(UserBase):
    """Pydantic model for creating a new user"""
    pass


class UserUpdate(BaseModel):
    """
    Pydantic model for updating an existing user.
    All fields are optional to allow partial updates.
    """
    userName: Optional[str] = Field(None, example="Updated Name Inc.", description="Updated name of the user")

class UserResponse(UserBase):
    """Pydantic model for user response that includes the ID"""
    userID: int = Field(..., example=1, description="Unique identifier for the user")
    
    model_config = {
        "from_attributes": True
    }
