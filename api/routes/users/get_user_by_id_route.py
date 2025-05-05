from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.user import UserResponse
from services.users.get_user_by_id_service import get_user_by_id
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_200_OK: {"description": "User Retrieved Successfully"}
    }
)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a user by ID",
    response_description="The requested user"
)
async def get_user_endpoint(
    user_id: int = Path(..., title="User ID", description="ID of the user to retrieve", gt=0),
    db: Session = Depends(get_db)
):
    """
    Retrieve a single user by its ID.
    
    Parameters:
    - **user_id**: ID of the user to retrieve (path parameter)
    
    Returns:
    - **UserResponse**: The requested user
    
    Raises:
    - **404 Not Found**: If the user with the given ID doesn't exist
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    try:
        user = get_user_by_id(db, user_id)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
            
        return user
        
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