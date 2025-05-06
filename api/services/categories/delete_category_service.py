import logging
from typing import Tuple, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.category import Category

# Set up logging
logger = logging.getLogger(__name__)

def delete_category(db: Session, category_id: int) -> Tuple[bool, Optional[str]]:
    """
    Delete a category from the database by ID.
    
    Args:
        db: SQLAlchemy database session
        category_id: ID of the category to delete
        
    Returns:
        tuple: (success, error_message)
            - success: True if deletion was successful, False otherwise
            - error_message: None if successful, error message string if failed
        
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query the category by ID
        db_category = db.query(Category).filter(Category.categoryID == category_id).first()
        
        # Return False if Category not found
        if not db_category:
            logger.warning(f"Category with ID {category_id} not found for deletion")
            return False, f"Category with ID {category_id} not found"
        
        # Get Category name for logging
        category_name = db_category.categoryName
        
        # Delete the category
        db.delete(db_category)
        db.commit()
        
        logger.info(f"Deleted Category ID {category_id}: {category_name}")
        return True, None
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        error_msg = f"Database error when deleting Category {category_id}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        error_msg = f"Unexpected error when deleting Category {category_id}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

