"""
Initialize database tables for production deployment.
Run this once after deploying to create all necessary tables.
"""
import os
import logging
from database import init_db, check_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Initialize database tables."""
    logger.info("=" * 50)
    logger.info("DATABASE INITIALIZATION")
    logger.info("=" * 50)
    
    # Check if DATABASE_URL is set
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.error("❌ DATABASE_URL environment variable not set!")
        logger.error("Please set DATABASE_URL in your deployment platform")
        return False
    
    logger.info(f"✓ DATABASE_URL is set")
    logger.info(f"  Host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'unknown'}")
    
    # Check database connection
    logger.info("\nChecking database connection...")
    if not check_connection():
        logger.error("❌ Cannot connect to database!")
        logger.error("Please check:")
        logger.error("  1. Database is running")
        logger.error("  2. DATABASE_URL is correct")
        logger.error("  3. Database allows connections from this IP")
        return False
    
    logger.info("✓ Database connection successful")
    
    # Initialize database (create tables)
    logger.info("\nCreating database tables...")
    try:
        init_db()
        logger.info("✓ Database tables created successfully")
        logger.info("\nTables created:")
        logger.info("  - users")
        logger.info("  - conversations")
        logger.info("  - messages")
        logger.info("  - usage")
        
        logger.info("\n" + "=" * 50)
        logger.info("✅ DATABASE INITIALIZATION COMPLETE!")
        logger.info("=" * 50)
        logger.info("\nYour database is ready to use.")
        logger.info("Usage tracking will now work correctly.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating tables: {str(e)}")
        logger.error("\nPlease check the error above and try again.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
