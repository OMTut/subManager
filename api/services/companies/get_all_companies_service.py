from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from models.company import Company

# Set up logging
logger = logging.getLogger(__name__)

def get_all_companies(db: Session) -> List[Company]:
    """
    Retrieve all companies from the database.
    Args:
        db: SQLAlchemy database session
    Returns:
        List of Company objects
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query all companies from the database
        companies = db.query(Company).all()
        logger.info(f"Retrieved {len(companies)} companies from database")
        return companies
    except SQLAlchemyError as e:
        # Log the error and re-raise
        logger.error(f"Database error when retrieving companies: {str(e)}")
        raise