from typing import Union, List
import uvicorn
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Import database components
from services.db.connect_to_db import get_db
from models.company import Company

# Import routers
from routes.companies.get_all_companies_route import router as get_all_companies_router
from routes.companies.add_company_route import router as add_company_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Subscription Manager API",
    description="API for managing subscriptions",
    version="1.0.0"
)

# Include routers
app.include_router(get_all_companies_router)
app.include_router(add_company_router)


if __name__ == "__main__":
    """
    Run the FastAPI application with Uvicorn server.
    
    This allows you to run the application directly with:
    $ python main.py
    
    Alternatively, you can still use the Uvicorn command:
    $ uvicorn main:app --reload
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Listen on all available network interfaces
        port=8000,       # Port to run the server on
        reload=True,     # Auto-reload when files change
        log_level="info" # Log level
    )