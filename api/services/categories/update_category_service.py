from typing import Optional, Dict, Any
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.category import Category, CategoryUpdate

# Set up logging
logger = logging.getLogger(__name__)

def update_category(db: Session, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
    """
    Update an existing Category in the database.
    
    Args:
        db: SQLAlchemy database session
        category_id: ID of the Category to update
        category_data: Validated Category data for update
        
    Returns:
        Category: The updated Category object, or None if not found
        
    Raises:
        SQLAlchemyError: If there is a database error
        IntegrityError: If there is a constraint violation
        ValueError: If the Category data is invalid
    """
    try:
        # Query the Category by ID
        db_category = db.query(Category).filter(Category.categoryID == category_id).first()
        
        # Return None if category not found
        if not db_category:
            logger.warning(f"Category with ID {category_id} not found for update")
            return None
        
        # Update category data if provided
        update_data = category_data.dict(exclude_unset=True)
        
        if update_data:
            # Special handling for URL to convert Pydantic HttpUrl to string
            if 'categoryURL' in update_data and update_data['categoryURL'] is not None:
                update_data['categoryURL'] = str(update_data['categoryURL'])
                
            for key, value in update_data.items():
                setattr(db_category, key, value)
                
            # Commit changes to database
            db.commit()
            db.refresh(db_category)
            
            logger.info(f"Updated category ID {category_id}: {db_category.categoryName}")
        else:
            logger.info(f"No changes provided for category ID {category_id}")
            
        return db_category
        
    except IntegrityError as e:
        # Roll back the session in case of integrity error
        db.rollback()
        logger.error(f"Integrity error when updating category {category_id}: {str(e)}")
        raise
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        logger.error(f"Database error when updating category {category_id}: {str(e)}")
        raise
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        logger.error(f"Unexpected error when updating category {category_id}: {str(e)}")
        raise ValueError(f"Error updating category: {str(e)}")

