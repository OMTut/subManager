from typing import Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.company import Company

# Set up logging
logger = logging.getLogger(__name__)

def get_company_by_id(db: Session, company_id: int) -> Optional[Company]:
    """
    Retrieve a single company by ID from the database.
    
    Args:
        db: SQLAlchemy database session
        company_id: ID of the company to retrieve
        
    Returns:
        Optional[Company]: The company if found, None otherwise
        
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query the company by ID
        company = db.query(Company).filter(Company.companyId == company_id).first()
        
        if company:
            logger.info(f"Retrieved company ID {company_id}: {company.companyName}")
        else:
            logger.warning(f"Company with ID {company_id} not found")
            
        return company
        
    except SQLAlchemyError as e:
        # Log the error and re-raise
        logger.error(f"Database error when retrieving company {company_id}: {str(e)}")
        raise
        
    except Exception as e:
        # Log the error and re-raise
        logger.error(f"Unexpected error when retrieving company {company_id}: {str(e)}")
        raise ValueError(f"Error retrieving company: {str(e)}")