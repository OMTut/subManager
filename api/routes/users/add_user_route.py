from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.user import UserCreate, UserResponse
from services.users.add_user_service import add_user
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_201_CREATED: {"description": "User Created Successfully"}
    }
)

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="The created user"
)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user in the database.
    
    Parameters:
    - **user**: user data including name and optional URL
    
    Returns:
    - **UserResponse**: The created user with its assigned ID
    
    Raises:
    - **400 Bad Request**: If the user data is invalid or a duplicate
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    try:
        new_user = add_user(db, user)
        return new_user
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists or constraint violation"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )