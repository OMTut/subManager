from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from models.subscription import Subscription

# Set up logging
logger = logging.getLogger(__name__)

def get_all_subscriptions(db: Session) -> List[Subscription]:
    """
    Retrieve all subscriptions from the database.
    Args:
        db: SQLAlchemy database session
    Returns:
        List of Subscription objects
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query all subscriptions from the database
        subscriptions = db.query(Subscription).all()
        logger.info(f"Retrieved {len(subscriptions)} subscriptions from database")
        return subscriptions
    except SQLAlchemyError as e:
        # Log the error and re-raise
        logger.error(f"Database error when retrieving subscriptions: {str(e)}")
        raise