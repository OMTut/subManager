from typing import Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.user import User, UserCreate

# Set up logging
logger = logging.getLogger(__name__)

def add_user(db: Session, user_data: UserCreate) -> User:
    """
    Add a new user to the database.
    
    Args:
        db: SQLAlchemy database session
        user_data: Validated user data from request
        
    Returns:
        user: The newly created user object
        
    Raises:
        SQLAlchemyError: If there is a database error
        IntegrityError: If there is a constraint violation (e.g., duplicate user)
        ValueError: If the user data is invalid
    """
    try:
        # Create a new User object from the validated data
        db_user = User(
            userName=user_data.userName
        )
        
        # Add to session and commit to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"Created new user: {db_user.userName} (ID: {db_user.userID})")
        return db_user
        
    except IntegrityError as e:
        # Roll back the session in case of integrity error
        db.rollback()
        logger.error(f"Integrity error when creating user: {str(e)}")
        raise
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        logger.error(f"Database error when creating user: {str(e)}")
        raise
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        logger.error(f"Unexpected error when creating user: {str(e)}")
        raise ValueError(f"Error creating user: {str(e)}")