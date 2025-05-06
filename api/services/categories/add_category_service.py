from typing import Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.category import Category, CategoryCreate

# Set up logging
logger = logging.getLogger(__name__)

def add_category(db: Session, category_data: CategoryCreate) -> Category:
    """
    Add a new category to the database.
    
    Args:
        db: SQLAlchemy database session
        category_data: Validated category data from request
        
    Returns:
        category: The newly created category object
        
    Raises:
        SQLAlchemyError: If there is a database error
        IntegrityError: If there is a constraint violation (e.g., duplicate category)
        ValueError: If the category data is invalid
    """
    try:
        # Create a new Category object from the validated data
        db_category = Category(
            categoryName=category_data.categoryName
        )
        
        # Add to session and commit to database
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        
        logger.info(f"Created new category: {db_category.categoryName} (ID: {db_category.categoryID})")
        return db_category
        
    except IntegrityError as e:
        # Roll back the session in case of integrity error
        db.rollback()
        logger.error(f"Integrity error when creating category: {str(e)}")
        raise
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        logger.error(f"Database error when creating category: {str(e)}")
        raise
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        logger.error(f"Unexpected error when creating category: {str(e)}")
        raise ValueError(f"Error creating category: {str(e)}")