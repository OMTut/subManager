from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from models.user import User

# Set up logging
logger = logging.getLogger(__name__)

def get_all_users(db: Session) -> List[User]:
    """
    Retrieve all users from the database.
    Args:
        db: SQLAlchemy database session
    Returns:
        List of User objects
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query all users from the database
        users = db.query(User).all()
        logger.info(f"Retrieved {len(users)} users from database")
        return users
    except SQLAlchemyError as e:
        # Log the error and re-raise
        logger.error(f"Database error when retrieving users: {str(e)}")
        raise