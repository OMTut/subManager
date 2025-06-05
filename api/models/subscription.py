from sqlalchemy import Column, Integer, String, Boolean, Text, Float, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, HttpUrl, Field, EmailStr
from typing import Optional

Base = declarative_base()

class Subscription(Base):
    """
    SQLAlchemy model for the subscriptions table.
    
    Attributes:
        subscriptionID: Primary key
        companyName: Company name
        price: price
        subscriptionCategory: Subscription category
        description: description
        userName: name the sub is under
        emailAssociated: email used for the sub account
    """
    __tablename__ = "subscriptions"
    
    subscriptionID = Column(Integer, primary_key=True, index=True)
    companyName = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)  # 10 digits total, 2 decimal places
    subscriptionCategory = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    userName = Column(String, nullable=True)
    emailAssociated = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Subscription {self.subscriptionID}: {self.companyName}>"


# Pydantic models for API request/response validation
class SubscriptionBase(BaseModel):
    """Base Pydantic model for subscription data"""
    companyName: str = Field(..., example="Netflix", description="Name of the subscription service")
    price: float = Field(..., example=9.99, description="Monthly price of the subscription")
    subscriptionCategory: Optional[str] = Field(None, example="Entertainment", description="Category of the subscription")
    description: Optional[str] = Field(None, example="Premium streaming plan", description="Description of the subscription")
    userName: Optional[str] = Field(None, example="John Doe", description="Name the subscription is under")
    emailAssociated: Optional[str] = Field(None, example="john.doe@example.com", description="Email used for the subscription account")


class SubscriptionCreate(SubscriptionBase):
    """Pydantic model for creating a new subscription"""
    pass


class SubscriptionUpdate(BaseModel):
    """
    Pydantic model for updating an existing subscription.
    All fields are optional to allow partial updates.
    """
    companyName: Optional[str] = Field(None, example="Netflix", description="Name of the subscription service")
    price: Optional[float] = Field(None, example=9.99, description="Monthly price of the subscription")
    subscriptionCategory: Optional[str] = Field(None, example="Entertainment", description="Category of the subscription")
    description: Optional[str] = Field(None, example="Premium streaming plan", description="Description of the subscription")
    userName: Optional[str] = Field(None, example="John Doe", description="Name the subscription is under")
    emailAssociated: Optional[str] = Field(None, example="john.doe@example.com", description="Email used for the subscription account")


class SubscriptionResponse(SubscriptionBase):
    """Pydantic model for subscription response that includes the ID"""
    subscriptionID: int = Field(..., example=1, description="Unique identifier for the subscription")
    
    model_config = {
        "from_attributes": True
    }
