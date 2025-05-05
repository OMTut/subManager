from typing import Union, List
import uvicorn
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Import database components
from services.db.connect_to_db import get_db
# from models.company import Company
# from models.user import User

# Import routers
from routes.companies.get_all_companies_route import router as get_all_companies_router
from routes.companies.add_company_route import router as add_company_router
from routes.companies.update_company_route import router as update_company_router
from routes.companies.delete_company_route import router as delete_company_router
from routes.companies.get_company_by_id_route import router as get_company_by_id_router
from routes.users.get_all_users_route import router as get_all_user_router
from routes.users.add_user_route import router as add_user_router
from routes.users.update_user_route import router as update_user_router
from routes.users.delete_user_route import router as delete_user_router
from routes.users.get_user_by_id_route import router as get_user_by_id_router

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
app.include_router(update_company_router)
app.include_router(delete_company_router)
app.include_router(get_company_by_id_router)
app.include_router(get_all_user_router)
app.include_router(add_user_router)
app.include_router(update_user_router)
app.include_router(delete_user_router)
app.include_router(get_user_by_id_router)


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