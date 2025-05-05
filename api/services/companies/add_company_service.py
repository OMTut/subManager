from typing import Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.company import Company, CompanyCreate

# Set up logging
logger = logging.getLogger(__name__)

def add_company(db: Session, company_data: CompanyCreate) -> Company:
    """
    Add a new company to the database.
    
    Args:
        db: SQLAlchemy database session
        company_data: Validated company data from request
        
    Returns:
        Company: The newly created company object
        
    Raises:
        SQLAlchemyError: If there is a database error
        IntegrityError: If there is a constraint violation (e.g., duplicate company)
        ValueError: If the company data is invalid
    """
    try:
        # Create a new Company object from the validated data
        db_company = Company(
            companyName=company_data.companyName,
            companyURL=str(company_data.companyURL) if company_data.companyURL else None
        )
        
        # Add to session and commit to database
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        
        logger.info(f"Created new company: {db_company.companyName} (ID: {db_company.companyId})")
        return db_company
        
    except IntegrityError as e:
        # Roll back the session in case of integrity error
        db.rollback()
        logger.error(f"Integrity error when creating company: {str(e)}")
        raise
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        logger.error(f"Database error when creating company: {str(e)}")
        raise
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        logger.error(f"Unexpected error when creating company: {str(e)}")
        raise ValueError(f"Error creating company: {str(e)}")