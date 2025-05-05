from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from services.users.get_all_users_service import get_all_users
from services.db.connect_to_db import get_db  # Adjust import path based on your project structure

# Create router for user endpoints
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={500: {"description": "Internal Server Error"}}
)

@router.get("/", response_model=List[dict])
async def read_users(db: Session = Depends(get_db)):
    """
    Get all users from the database.
    
    Returns:
        List of users
    """
    try:
        users = get_all_users(db)
        # Convert SQLAlchemy models to dictionaries for JSON response
        return [
            {
                "id": user.userID,
                "name": user.userName,
            } 
            for user in users
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