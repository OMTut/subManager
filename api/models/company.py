from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

Base = declarative_base()

class Company(Base):
    """
    SQLAlchemy model for the companies table.
    
    Attributes:
        companyId: Primary key
        companyName: Company name
        companyURL: Company website URL
    """
    __tablename__ = "companies"
    
    companyId = Column(Integer, primary_key=True, index=True)
    companyName = Column(String, nullable=True)  # character varying in PostgreSQL
    companyURL = Column(Text, nullable=True)     # text in PostgreSQL
    
    def __repr__(self):
        return f"<Company {self.companyName}>"


# Pydantic models for API request/response validation
class CompanyBase(BaseModel):
    """Base Pydantic model for company data"""
    companyName: str = Field(..., example="Acme Inc.", description="Name of the company")
    companyURL: Optional[HttpUrl] = Field(None, example="https://acme.com", description="Company website URL")


class CompanyCreate(CompanyBase):
    """Pydantic model for creating a new company"""
    pass


class CompanyResponse(CompanyBase):
    """Pydantic model for company response that includes the ID"""
    companyId: int = Field(..., example=1, description="Unique identifier for the company")
    
    class Config:
        orm_mode = True
