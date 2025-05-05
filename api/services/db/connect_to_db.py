import logging
from typing import Generator, Dict
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .config import load_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create SQLAlchemy Base
Base = declarative_base()

def get_database_url() -> str:
    """
    Create a database URL from the config values.
    Properly URL encodes parameters, especially the password which may contain special characters.
    
    Returns:
        str: A properly formatted and URL-encoded database connection string
        
    Raises:
        KeyError: If required configuration values are missing
        Exception: For other errors during URL construction
    """
    try:
        config = load_config()
        
        # Validate required config parameters
        required_params = ['user', 'password', 'host', 'port', 'database']
        for param in required_params:
            if param not in config or not config[param]:
                raise KeyError(f"Missing required database configuration parameter: {param}")
        
        # URL encode the username and password to handle special characters
        username = urllib.parse.quote_plus(config['user'])
        password = urllib.parse.quote_plus(config['password'])
        
        # Construct and return the connection URL
        connection_url = f"postgresql://{username}:{password}@{config['host']}:{config['port']}/{config['database']}"
        logger.debug(f"Database URL created successfully (sensitive info redacted)")
        return connection_url
    except KeyError as ke:
        logger.error(f"Configuration error: {ke}")
        raise
    except Exception as e:
        logger.error(f"Error creating database URL: {e}")
        raise

# Create SQLAlchemy engine
try:
    engine = create_engine(get_database_url())
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    raise

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get a database session for FastAPI endpoints.
    Ensures the session is properly closed even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session provided")
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()
        logger.debug("Database session closed")

if __name__ == '__main__':
    # Test connection
    with SessionLocal() as session:
        try:
            # Execute a simple query to test the connection
            session.execute("SELECT 1")
            logger.info("Connection successful!")
        except Exception as e:
            logger.error(f"An error occurred while connecting to the database: {e}")
