from typing import Optional, Dict, Any
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.user import User, UserUpdate

# Set up logging
logger = logging.getLogger(__name__)

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """
    Update an existing User in the database.
    
    Args:
        db: SQLAlchemy database session
        user_id: ID of the User to update
        user_data: Validated User data for update
        
    Returns:
        User: The updated User object, or None if not found
        
    Raises:
        SQLAlchemyError: If there is a database error
        IntegrityError: If there is a constraint violation
        ValueError: If the User data is invalid
    """
    try:
        # Query the User by ID
        db_User = db.query(User).filter(User.userID == user_id).first()
        
        # Return None if user not found
        if not db_User:
            logger.warning(f"User with ID {user_id} not found for update")
            return None
        
        # Update user data if provided
        update_data = user_data.dict(exclude_unset=True)
        
        if update_data:
            # Special handling for URL to convert Pydantic HttpUrl to string
            if 'userURL' in update_data and update_data['userURL'] is not None:
                update_data['userURL'] = str(update_data['userURL'])
                
            for key, value in update_data.items():
                setattr(db_User, key, value)
                
            # Commit changes to database
            db.commit()
            db.refresh(db_User)
            
            logger.info(f"Updated user ID {user_id}: {db_User.userName}")
        else:
            logger.info(f"No changes provided for user ID {user_id}")
            
        return db_User
        
    except IntegrityError as e:
        # Roll back the session in case of integrity error
        db.rollback()
        logger.error(f"Integrity error when updating user {user_id}: {str(e)}")
        raise
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        logger.error(f"Database error when updating user {user_id}: {str(e)}")
        raise
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        logger.error(f"Unexpected error when updating user {user_id}: {str(e)}")
        raise ValueError(f"Error updating user: {str(e)}")

