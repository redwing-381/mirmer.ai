"""
Database connection and session management for PostgreSQL.
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

# SQLAlchemy Base for models
Base = declarative_base()

# Database engine and session (only if DATABASE_URL is set)
engine = None
SessionLocal = None

if DATABASE_URL:
    try:
        # Create engine with connection pooling
        engine = create_engine(
            DATABASE_URL,
            pool_size=5,              # Number of persistent connections
            max_overflow=10,          # Additional connections during peak load
            pool_pre_ping=True,       # Verify connections before using
            pool_recycle=3600,        # Recycle connections after 1 hour
            echo=False                # Set to True for SQL query logging
        )
        
        # Create session factory
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
        
        logger.info("PostgreSQL database connection configured")
        logger.info(f"Connection pool: size=5, max_overflow=10")
        
    except Exception as e:
        logger.error(f"Failed to configure database connection: {e}")
        engine = None
        SessionLocal = None
else:
    logger.info("DATABASE_URL not set - PostgreSQL not configured")


def init_db():
    """
    Initialize database by creating all tables.
    This is called on application startup.
    """
    if engine is None:
        logger.warning("Cannot initialize database: engine not configured")
        return False
    
    try:
        # Import models to register them with Base
        import models
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False


def get_db():
    """
    Get database session for dependency injection.
    Yields a session and ensures it's closed after use.
    """
    if SessionLocal is None:
        raise RuntimeError("Database not configured - DATABASE_URL not set")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection():
    """
    Check if database connection is working.
    Returns True if connection is successful, False otherwise.
    """
    if engine is None:
        return False
    
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False
