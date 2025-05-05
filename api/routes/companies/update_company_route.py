from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.company import CompanyUpdate, CompanyResponse
from services.companies.update_company_service import update_company
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Company Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_200_OK: {"description": "Company Updated Successfully"}
    }
)

@router.put(
    "/{company_id}",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing company",
    response_description="The updated company"
)
async def update_company_endpoint(
    company_id: int = Path(..., title="Company ID", description="ID of the company to update", gt=0),
    company: CompanyUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Update an existing company in the database.
    
    Parameters:
    - **company_id**: ID of the company to update (path parameter)
    - **company**: Updated company data (request body)
    
    Returns:
    - **CompanyResponse**: The updated company
    
    Raises:
    - **404 Not Found**: If the company with the given ID doesn't exist
    - **400 Bad Request**: If the company data is invalid or a constraint violation occurs
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    if company is None:
        company = CompanyUpdate()
        
    try:
        updated_company = update_company(db, company_id, company)
        
        if updated_company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company with ID {company_id} not found"
            )
            
        return updated_company
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company update failed due to constraint violation"
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

