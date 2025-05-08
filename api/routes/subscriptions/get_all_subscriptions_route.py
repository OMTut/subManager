from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from services.subscriptions.get_all_subscriptions_service import get_all_subscriptions
from services.db.connect_to_db import get_db  # Adjust import path based on your project structure

# Create router for company endpoints
router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    responses={500: {"description": "Internal Server Error"}}
)

@router.get("/", response_model=List[dict])
async def read_subscriptions(db: Session = Depends(get_db)):
    """
    Get all subscriptions from the database.
    
    Returns:
        List of subscriptions
    """
    try:
        subscriptions = get_all_subscriptions(db)
        # Convert SQLAlchemy models to dictionaries for JSON response
        return [
            {
                "id": subscription.subscriptionID,
                "name": subscription.companyName,
                "price": subscription.price,
                "category": subscription.subscriptionCategory,
                "description": subscription.description,
                "account_holder": subscription.userName,
                "account_email": subscription.emailAssociated
            } 
            for subscription in subscriptions
        ]
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred: {str(e)}"
        )