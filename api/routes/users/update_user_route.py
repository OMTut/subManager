from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.user import UserUpdate, UserResponse
from services.users.update_user_service import update_user
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_200_OK: {"description": "User Updated Successfully"}
    }
)

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing company",
    response_description="The updated company"
)
async def update_company_endpoint(
    user_id: int = Path(..., title="User ID", description="ID of the user to update", gt=0),
    user: UserUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Update an existing user in the database.
    
    Parameters:
    - **user_id**: ID of the user to update (path parameter)
    - **user**: Updated user data (request body)
    
    Returns:
    - **UserResponse**: The updated user
    
    Raises:
    - **404 Not Found**: If the user with the given ID doesn't exist
    - **400 Bad Request**: If the user data is invalid or a constraint violation occurs
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    if user is None:
        user = UserUpdate()
        
    try:
        updated_user = update_user(db, user_id, user)
        
        if updated_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with ID {user_id} not found"
            )
            
        return updated_user
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user update failed due to constraint violation"
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

