from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.subscription import SubscriptionUpdate, SubscriptionResponse
from services.subscriptions.update_subscription_service import update_subscription
from services.db.connect_to_db import get_db

# Create router
router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Subscription Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_200_OK: {"description": "Subscription Updated Successfully"}
    }
)

@router.put(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing subsciption",
    response_description="The updated subsciption"
)
async def update_subscription_endpoint(
    subscription_id: int = Path(..., title="Subscription ID", description="ID of the subsciption to update", gt=0),
    subsciption: SubscriptionUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Update an existing subsciption in the database.
    
    Parameters:
    - **subscription_id**: ID of the subsciption to update (path parameter)
    - **subsciption**: Updated subsciption data (request body)
    
    Returns:
    - **SubscriptionResponse**: The updated subsciption
    
    Raises:
    - **404 Not Found**: If the subsciption with the given ID doesn't exist
    - **400 Bad Request**: If the subsciption data is invalid or a constraint violation occurs
    - **500 Internal Server Error**: If there's an error with the database or server
    """
    if subsciption is None:
        subsciption = SubscriptionUpdate()
        
    try:
        updated_subsciption = update_subscription(db, subscription_id, subsciption)
        
        if updated_subsciption is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subscription with ID {subscription_id} not found"
            )
            
        return updated_subsciption
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subscription update failed due to constraint violation"
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

