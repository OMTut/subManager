from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

Base = declarative_base()

class Category(Base):
    """
    SQLAlchemy model for the categories table.
    
    Attributes:
        categoryD: Primary key
        categoryName: User name
    """
    __tablename__ = "categories"
    
    categoryID = Column(Integer, primary_key=True, index=True)
    categoryName = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<User {self.categoryName}>"


# Pydantic models for API request/response validation
class CategoryBase(BaseModel):
    """Base Pydantic model for category data"""
    categoryName: str = Field(..., example="Acme Inc.", description="Name of the category")


class UserCreate(CategoryBase):
    """Pydantic model for creating a new category"""
    pass


class UserUpdate(BaseModel):
    """
    Pydantic model for updating an existing category.
    All fields are optional to allow partial updates.
    """
    categoryName: Optional[str] = Field(None, example="Updated Name Inc.", description="Updated name of the category")

class CategoryResponse(CategoryBase):
    """Pydantic model for category response that includes the ID"""
    categoryID: int = Field(..., example=1, description="Unique identifier for the category")
    
    model_config = {
        "from_attributes": True
    }