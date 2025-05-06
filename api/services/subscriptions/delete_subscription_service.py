import logging
from typing import Tuple, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.subscription import Subscription

# Set up logging
logger = logging.getLogger(__name__)

def delete_subscription(db: Session, subscription_id: int) -> Tuple[bool, Optional[str]]:
    """
    Delete a subscription from the database by ID.
    
    Args:
        db: SQLAlchemy database session
        subscription_id: ID of the subscription to delete
        
    Returns:
        tuple: (success, error_message)
            - success: True if deletion was successful, False otherwise
            - error_message: None if successful, error message string if failed
        
    Raises:
        SQLAlchemyError: If there is a database error
    """
    try:
        # Query the subscription by ID
        db_subscription = db.query(Subscription).filter(Subscription.subscriptionID == subscription_id).first()
        
        # Return False if subscription not found
        if not db_subscription:
            logger.warning(f"Subscription with ID {subscription_id} not found for deletion")
            return False, f"Subscription with ID {subscription_id} not found"
        
        # Get subscription name for logging
        company_name = db_subscription.companyName
        
        # Delete the subscription
        db.delete(db_subscription)
        db.commit()
        
        logger.info(f"Deleted subscription ID {subscription_id}: {company_name}")
        return True, None
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        error_msg = f"Database error when deleting subscription {subscription_id}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        error_msg = f"Unexpected error when deleting subscription {subscription_id}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

