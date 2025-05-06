from typing import Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.subscription import Subscription, SubscriptionCreate

# Set up logging
logger = logging.getLogger(__name__)

def add_subscription(db: Session, subscription_data: SubscriptionCreate) -> Subscription:
    """
    Add a new subscription to the database.
    
    Args:
        db: SQLAlchemy database session
        subscription_data: Validated subscription data from request
        
    Returns:
        Subscription: The newly created subscription object
        
    Raises:
        SQLAlchemyError: If there is a database error
        IntegrityError: If there is a constraint violation (e.g., duplicate subscription)
        ValueError: If the subscription data is invalid
    """
    try:
        # Create a new Subscription object from the validated data
        db_subscription = Subscription(
            companyName=subscription_data.companyName,
            price=subscription_data.price,
            subscriptionCategory=subscription_data.subscriptionCategory,
            description=subscription_data.description,
            userName=subscription_data.userName,
            emailAssociated=subscription_data.emailAssociated
        )
        
        # Add to session and commit to database
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        
        logger.info(f"Created new subscription: {db_subscription.companyName} (ID: {db_subscription.subscriptionID})")
        return db_subscription
        
    except IntegrityError as e:
        # Roll back the session in case of integrity error
        db.rollback()
        logger.error(f"Integrity error when creating subscription: {str(e)}")
        raise
        
    except SQLAlchemyError as e:
        # Roll back the session in case of database error
        db.rollback()
        logger.error(f"Database error when creating subscription: {str(e)}")
        raise
        
    except Exception as e:
        # Roll back the session in case of any other error
        db.rollback()
        logger.error(f"Unexpected error when creating subscription: {str(e)}")
        raise ValueError(f"Error creating subscription: {str(e)}")