from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.category import CategoryCreate, CategoryResponse
from services.categories.add_category_service import add_category
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_201_CREATED: {"description": "Category Created Successfully"}
    }
)

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
    response_description="The created category"
)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new category in the database.
    
    Parameters:
    - **category**: category data including name and optional URL
    
    Returns:
    - **CategoryResponse**: The created category with its assigned ID
    
    Raises:
    - **400 Bad Request**: If the category data is invalid or a duplicate
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    try:
        new_category = add_category(db, category)
        return new_category
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists or constraint violation"
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