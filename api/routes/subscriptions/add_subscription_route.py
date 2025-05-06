from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.subscription import SubscriptionCreate, SubscriptionResponse
from services.subscriptions.add_subscription_service import add_subscription
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_201_CREATED: {"description": "Subscription Created Successfully"}
    }
)

@router.post(
    "/",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new subscription",
    response_description="The created subscription"
)
async def create_company(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new subscription in the database.
    
    Parameters:
    - **subscription**: Subscription data including name and optional URL
    
    Returns:
    - **SubscriptionResponse**: The created subscription with its assigned ID
    
    Raises:
    - **400 Bad Request**: If the subscription data is invalid or a duplicate
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    try:
        new_subscription = add_subscription(db, subscription)
        return new_subscription
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subscription already exists or constraint violation"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )