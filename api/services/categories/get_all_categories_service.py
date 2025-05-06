from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from models.category import Category

# Set up logging
logger = logging.getLogger(__name__)

def get_all_categories(db: Session) -> List[Category]:
    """
    Retrieve all categories from the database.
    Args:
        db: SQLAlchemy database session
    Returns:
        List of Category objects
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query all categories from the database
        categories = db.query(Category).all()
        logger.info(f"Retrieved {len(categories)} categories from database")
        return categories
    except SQLAlchemyError as e:
        # Log the error and re-raise
        logger.error(f"Database error when retrieving categories: {str(e)}")
        raise