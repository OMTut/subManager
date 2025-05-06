from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.category import CategoryUpdate, CategoryResponse
from services.categories.update_category_service import update_category
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Category Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_200_OK: {"description": "Category Updated Successfully"}
    }
)

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing categroy",
    response_description="The updated categroy"
)
async def update_categroy_endpoint(
    category_id: int = Path(..., title="Category ID", description="ID of the category to update", gt=0),
    category: CategoryUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Update an existing category in the database.
    
    Parameters:
    - **category_id**: ID of the category to update (path parameter)
    - **category**: Updated category data (request body)
    
    Returns:
    - **CategoryResponse**: The updated category
    
    Raises:
    - **404 Not Found**: If the category with the given ID doesn't exist
    - **400 Bad Request**: If the category data is invalid or a constraint violation occurs
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    if category is None:
        category = CategoryUpdate()
        
    try:
        updated_category = update_category(db, category_id, category)
        
        if updated_category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"category with ID {category_id} not found"
            )
            
        return updated_category
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="category update failed due to constraint violation"
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

