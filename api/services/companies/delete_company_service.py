import logging
from typing import Tuple, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.company import Company

# Set up logging
logger = logging.getLogger(__name__)

def delete_company(db: Session, company_id: int) -> Tuple[bool, Optional[str]]:
    """
    Delete a company from the database by ID.
    
    Args:
        db: SQLAlchemy database session
        company_id: ID of the company to delete
        
    Returns:
        tuple: (success, error_message)
            - success: True if deletion was successful, False otherwise
            - error_message: None if successful, error message string if failed
        
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query the company by ID
        db_company = db.query(Company).filter(Company.companyId == company_id).first()
        
        # Return False if company not found
        if not db_company:
            logger.warning(f"Company with ID {company_id} not found for deletion")
            return False, f"Company with ID {company_id} not found"
        
        # Get company name for logging
        company_name = db_company.companyName
        
        # Delete the company
        db.delete(db_company)
        db.commit()
        
        logger.info(f"Deleted company ID {company_id}: {company_name}")
        return True, None
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        error_msg = f"Database error when deleting company {company_id}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        error_msg = f"Unexpected error when deleting company {company_id}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

