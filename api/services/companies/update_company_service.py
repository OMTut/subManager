from typing import Optional, Dict, Any
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.company import Company, CompanyUpdate

# Set up logging
logger = logging.getLogger(__name__)

def update_company(db: Session, company_id: int, company_data: CompanyUpdate) -> Optional[Company]:
    """
    Update an existing company in the database.
    
    Args:
        db: SQLAlchemy database session
        company_id: ID of the company to update
        company_data: Validated company data for update
        
    Returns:
        Company: The updated company object, or None if not found
        
    Raises:
        SQLAlchemyError: If there is a database error
        IntegrityError: If there is a constraint violation
        ValueError: If the company data is invalid
    """
    try:
        # Query the company by ID
        db_company = db.query(Company).filter(Company.companyId == company_id).first()
        
        # Return None if company not found
        if not db_company:
            logger.warning(f"Company with ID {company_id} not found for update")
            return None
        
        # Update company data if provided
        update_data = company_data.dict(exclude_unset=True)
        
        if update_data:
            # Special handling for URL to convert Pydantic HttpUrl to string
            if 'companyURL' in update_data and update_data['companyURL'] is not None:
                update_data['companyURL'] = str(update_data['companyURL'])
                
            for key, value in update_data.items():
                setattr(db_company, key, value)
                
            # Commit changes to database
            db.commit()
            db.refresh(db_company)
            
            logger.info(f"Updated company ID {company_id}: {db_company.companyName}")
        else:
            logger.info(f"No changes provided for company ID {company_id}")
            
        return db_company
        
    except IntegrityError as e:
        # Roll back the session in case of integrity error
        db.rollback()
        logger.error(f"Integrity error when updating company {company_id}: {str(e)}")
        raise
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        logger.error(f"Database error when updating company {company_id}: {str(e)}")
        raise
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        logger.error(f"Unexpected error when updating company {company_id}: {str(e)}")
        raise ValueError(f"Error updating company: {str(e)}")

