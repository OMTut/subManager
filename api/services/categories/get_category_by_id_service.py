from typing import Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.category import Category

# Set up logging
logger = logging.getLogger(__name__)

def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
    """
    Retrieve a single category by ID from the database.
    
    Args:
        db: SQLAlchemy database session
        category_id: ID of the category to retrieve
        
    Returns:
        Optional[Category]: The category if found, None otherwise
        
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query the category by ID
        category = db.query(Category).filter(Category.categoryID == category_id).first()
        
        if category:
            logger.info(f"Retrieved category ID {category_id}: {category.categoryName}")
        else:
            logger.warning(f"Category with ID {category_id} not found")
            
        return category
        
    except SQLAlchemyError as e:
        # Log the error and re-raise
        logger.error(f"Database error when retrieving category {category_id}: {str(e)}")
        raise
        
    except Exception as e:
        # Log the error and re-raise
        logger.error(f"Unexpected error when retrieving category {category_id}: {str(e)}")
        raise ValueError(f"Error retrieving category: {str(e)}")