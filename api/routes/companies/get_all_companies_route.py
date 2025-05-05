from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from services.companies.get_all_companies_service import get_all_companies
from services.db.connect_to_db import get_db  # Adjust import path based on your project structure

# Create router for company endpoints
router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={500: {"description": "Internal Server Error"}}
)

@router.get("/", response_model=List[dict])
async def read_companies(db: Session = Depends(get_db)):
    """
    Get all companies from the database.
    
    Returns:
        List of companies
    """
    try:
        companies = get_all_companies(db)
        # Convert SQLAlchemy models to dictionaries for JSON response
        return [
            {
                "id": company.companyId,
                "name": company.companyName,
                "url": company.companyURL
            } 
            for company in companies
        ]
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred: {str(e)}"
        )