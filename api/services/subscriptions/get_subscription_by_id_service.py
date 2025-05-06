from typing import Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.subscription import Subscription

# Set up logging
logger = logging.getLogger(__name__)

def get_subscription_by_id(db: Session, subscription_id: int) -> Optional[Subscription]:
    """
    Retrieve a single subscription by ID from the database.
    
    Args:
        db: SQLAlchemy database session
        subscription_id: ID of the subscription to retrieve
        
    Returns:
        Optional[Subscription]: The subscription if found, None otherwise
        
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query the subscription by ID
        subscription = db.query(Subscription).filter(Subscription.subscriptionID == subscription_id).first()
        
        if subscription:
            logger.info(f"Retrieved subscription ID {subscription_id}: {subscription.companyName}")
        else:
            logger.warning(f"Subscription with ID {subscription_id} not found")
            
        return subscription
        
    except SQLAlchemyError as e:
        # Log the error and re-raise
        logger.error(f"Database error when retrieving subscription {subscription_id}: {str(e)}")
        raise
        
    except Exception as e:
        # Log the error and re-raise
        logger.error(f"Unexpected error when retrieving subscription {subscription_id}: {str(e)}")
        raise ValueError(f"Error retrieving subscription: {str(e)}")