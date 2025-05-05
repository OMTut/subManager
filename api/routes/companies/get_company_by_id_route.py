from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.company import CompanyResponse
from services.companies.get_company_by_id_service import get_company_by_id
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Company Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_200_OK: {"description": "Company Retrieved Successfully"}
    }
)

@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a company by ID",
    response_description="The requested company"
)
async def get_company_endpoint(
    company_id: int = Path(..., title="Company ID", description="ID of the company to retrieve", gt=0),
    db: Session = Depends(get_db)
):
    """
    Retrieve a single company by its ID.
    
    Parameters:
    - **company_id**: ID of the company to retrieve (path parameter)
    
    Returns:
    - **CompanyResponse**: The requested company
    
    Raises:
    - **404 Not Found**: If the company with the given ID doesn't exist
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    try:
        company = get_company_by_id(db, company_id)
        
        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company with ID {company_id} not found"
            )
            
        return company
        
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