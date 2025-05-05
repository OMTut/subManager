import logging
from typing import Tuple, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.user import User

# Set up logging
logger = logging.getLogger(__name__)

def delete_user(db: Session, user_id: int) -> Tuple[bool, Optional[str]]:
    """
    Delete a user from the database by ID.
    
    Args:
        db: SQLAlchemy database session
        user_id: ID of the user to delete
        
    Returns:
        tuple: (success, error_message)
            - success: True if deletion was successful, False otherwise
            - error_message: None if successful, error message string if failed
        
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query the user by ID
        db_user = db.query(User).filter(User.userID == user_id).first()
        
        # Return False if User not found
        if not db_user:
            logger.warning(f"User with ID {user_id} not found for deletion")
            return False, f"User with ID {user_id} not found"
        
        # Get User name for logging
        user_name = db_user.userName
        
        # Delete the user
        db.delete(db_user)
        db.commit()
        
        logger.info(f"Deleted User ID {user_id}: {user_name}")
        return True, None
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        error_msg = f"Database error when deleting User {user_id}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        error_msg = f"Unexpected error when deleting User {user_id}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

