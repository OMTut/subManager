from typing import Optional, Dict, Any
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.subscription import Subscription, SubscriptionUpdate

# Set up logging
logger = logging.getLogger(__name__)

def update_subscription(db: Session, subscription_id: int, subscription_data: SubscriptionUpdate) -> Optional[Subscription]:
    """
    Update an existing subscription in the database.
    
    Args:
        db: SQLAlchemy database session
        subscription_id: ID of the subscription to update
        subscription_data: Validated subscription data for update
        
    Returns:
        Subscription: The updated subscription object, or None if not found
        
    Raises:
        SQLAlchemyError: If there is a database error
        IntegrityError: If there is a constraint violation
        ValueError: If the subscription data is invalid
    """
    try:
        # Query the subscription by ID
        db_subscription = db.query(Subscription).filter(Subscription.subscriptionID == subscription_id).first()
        
        # Return None if subscription not found
        if not db_subscription:
            logger.warning(f"Subscription with ID {subscription_id} not found for update")
            return None
        
        # Update subscription data if provided
        update_data = subscription_data.dict(exclude_unset=True)
        
        if update_data:               
            for key, value in update_data.items():
                setattr(db_subscription, key, value)
                
            # Commit changes to database
            db.commit()
            db.refresh(db_subscription)
            
            logger.info(f"Updated subscription ID {subscription_id}: {db_subscription.companyName}")
        else:
            logger.info(f"No changes provided for subscription ID {subscription_id}")
            
        return db_subscription
        
    except IntegrityError as e:
        # Roll back the session in case of integrity error
        db.rollback()
        logger.error(f"Integrity error when updating subscription {subscription_id}: {str(e)}")
        raise
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        logger.error(f"Database error when updating subscription {subscription_id}: {str(e)}")
        raise
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        logger.error(f"Unexpected error when updating subscription {subscription_id}: {str(e)}")
        raise ValueError(f"Error updating subscription: {str(e)}")

