from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.company import CompanyCreate, CompanyResponse
from services.companies.add_company_service import add_company
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_201_CREATED: {"description": "Company Created Successfully"}
    }
)

@router.post(
    "/",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company",
    response_description="The created company"
)
async def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new company in the database.
    
    Parameters:
    - **company**: Company data including name and optional URL
    
    Returns:
    - **CompanyResponse**: The created company with its assigned ID
    
    Raises:
    - **400 Bad Request**: If the company data is invalid or a duplicate
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    try:
        new_company = add_company(db, company)
        return new_company
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company already exists or constraint violation"
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