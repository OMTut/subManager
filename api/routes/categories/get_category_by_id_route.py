from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.category import CategoryResponse
from services.categories.get_category_by_id_service import get_category_by_id
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Category Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_200_OK: {"description": "Category Retrieved Successfully"}
    }
)

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a category by ID",
    response_description="The requested category"
)
async def get_category_endpoint(
    category_id: int = Path(..., title="Category ID", description="ID of the category to retrieve", gt=0),
    db: Session = Depends(get_db)
):
    """
    Retrieve a single category by its ID.
    
    Parameters:
    - **category_id**: ID of the category to retrieve (path parameter)
    
    Returns:
    - **CategoryResponse**: The requested category
    
    Raises:
    - **404 Not Found**: If the category with the given ID doesn't exist
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    try:
        category = get_category_by_id(db, category_id)
        
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
            
        return category
        
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