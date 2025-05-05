from fastapi import APIRouter, Depends, HTTPException, status, Path, Response
from sqlalchemy.orm import Session

from services.users.delete_user_service import delete_user
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_204_NO_CONTENT: {"description": "User Deleted Successfully"}
    }
)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    response_description="No content is returned on successful deletion"
)
async def delete_company_endpoint(
    user_id: int = Path(..., title="Company ID", description="ID of the user to delete", gt=0),
    db: Session = Depends(get_db)
):
    """
    Delete a user from the database.
    
    Parameters:
    - **user_id**: ID of the user to delete (path parameter)
    
    Returns:
    - No content (204) on successful deletion
    
    Raises:
    - **404 Not Found**: If the user with the given ID doesn't exist
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    success, error_message = delete_user(db, user_id)
    
    if not success:
        if "not found" in error_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_message
            )
    
    # Return 204 No Content for successful deletion
    return Response(status_code=status.HTTP_204_NO_CONTENT)

