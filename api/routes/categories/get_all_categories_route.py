from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from services.categories.get_all_categories_service import get_all_categories
from services.db.connect_to_db import get_db  # Adjust import path based on your project structure

# Create router for category endpoints
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={500: {"description": "Internal Server Error"}}
)

@router.get("/", response_model=List[dict])
async def read_categories(db: Session = Depends(get_db)):
    """
    Get all categories from the database.
    
    Returns:
        List of categories
    """
    try:
        categories = get_all_categories(db)
        # Convert SQLAlchemy models to dictionaries for JSON response
        return [
            {
                "id": category.categoryID,
                "name": category.categoryName,
            } 
            for category in categories
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