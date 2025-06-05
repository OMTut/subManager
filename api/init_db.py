#!/usr/bin/env python3
"""
Database initialization script for Subscription Manager API.

This script creates all database tables based on SQLAlchemy models.
Run this script to set up the database schema.

Usage:
    python init_db.py
"""

import logging
from sqlalchemy import create_engine
from services.db.connect_to_db import get_database_url, Base

# Import all models to ensure they're registered with Base.metadata
from models.company import Company
from models.user import User
from models.category import Category
from models.subscription import Subscription

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """
    Create all database tables based on SQLAlchemy models.
    """
    try:
        # Create database engine
        engine = create_engine(get_database_url())
        logger.info("Database engine created successfully")
        
        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
        # List all created tables
        table_names = list(Base.metadata.tables.keys())
        logger.info(f"Created tables: {', '.join(table_names)}")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def drop_tables():
    """
    Drop all database tables. Use with caution!
    """
    try:
        # Create database engine
        engine = create_engine(get_database_url())
        logger.info("Database engine created successfully")
        
        # Drop all tables
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully!")
        
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_tables()
    else:
        create_tables()

