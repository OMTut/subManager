from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.subscription import SubscriptionResponse
from services.subscriptions.get_subscription_by_id_service import get_subscription_by_id
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Subscription Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_200_OK: {"description": "Subscription Retrieved Successfully"}
    }
)

@router.get(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a subscription by ID",
    response_description="The requested subscription"
)
async def get_company_endpoint(
    subscription_id: int = Path(..., title="Subscription ID", description="ID of the subscription to retrieve", gt=0),
    db: Session = Depends(get_db)
):
    """
    Retrieve a single subscription by its ID.
    
    Parameters:
    - **subscription_id**: ID of the subscription to retrieve (path parameter)
    
    Returns:
    - **SubscriptionResponse**: The requested subscription
    
    Raises:
    - **404 Not Found**: If the subscription with the given ID doesn't exist
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    try:
        subscription = get_subscription_by_id(db, subscription_id)
        
        if subscription is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subscription with ID {subscription_id} not found"
            )
            
        return subscription
        
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