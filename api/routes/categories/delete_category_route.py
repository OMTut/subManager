from fastapi import APIRouter, Depends, HTTPException, status, Path, Response
from sqlalchemy.orm import Session

from services.categories.delete_category_service import delete_category
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Category Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_204_NO_CONTENT: {"description": "Category Deleted Successfully"}
    }
)

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category",
    response_description="No content is returned on successful deletion"
)
async def delete_category_endpoint(
    category_id: int = Path(..., title="Category ID", description="ID of the category to delete", gt=0),
    db: Session = Depends(get_db)
):
    """
    Delete a category from the database.
    
    Parameters:
    - **category_id**: ID of the category to delete (path parameter)
    
    Returns:
    - No content (204) on successful deletion
    
    Raises:
    - **404 Not Found**: If the category with the given ID doesn't exist
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    success, error_message = delete_category(db, category_id)
    
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

