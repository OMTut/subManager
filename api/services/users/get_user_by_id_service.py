from typing import Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.user import User

# Set up logging
logger = logging.getLogger(__name__)

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Retrieve a single user by ID from the database.
    
    Args:
        db: SQLAlchemy database session
        user_id: ID of the user to retrieve
        
    Returns:
        Optional[User]: The user if found, None otherwise
        
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query the user by ID
        user = db.query(User).filter(User.userID == user_id).first()
        
        if user:
            logger.info(f"Retrieved user ID {user_id}: {user.userName}")
        else:
            logger.warning(f"User with ID {user_id} not found")
            
        return user
        
    except SQLAlchemyError as e:
        # Log the error and re-raise
        logger.error(f"Database error when retrieving user {user_id}: {str(e)}")
        raise
        
    except Exception as e:
        # Log the error and re-raise
        logger.error(f"Unexpected error when retrieving user {user_id}: {str(e)}")
        raise ValueError(f"Error retrieving user: {str(e)}")