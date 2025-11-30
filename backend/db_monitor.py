"""
Database monitoring utilities for PostgreSQL.
"""
import logging
import time
from functools import wraps
from database import engine, SessionLocal

logger = logging.getLogger(__name__)

# Slow query threshold (in seconds)
SLOW_QUERY_THRESHOLD = 1.0


def log_slow_query(func):
    """
    Decorator to log slow database queries.
    Logs a warning if query takes longer than SLOW_QUERY_THRESHOLD.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            if duration > SLOW_QUERY_THRESHOLD:
                logger.warning(
                    f"Slow query detected: {func.__name__} took {duration:.2f}s "
                    f"(threshold: {SLOW_QUERY_THRESHOLD}s)"
                )
    return wrapper


def get_connection_pool_status():
    """
    Get current connection pool status.
    
    Returns:
        dict with pool statistics
    """
    if engine is None:
        return {"error": "Database not configured"}
    
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "total_connections": pool.size() + pool.overflow()
    }


def log_pool_status():
    """Log current connection pool status."""
    status = get_connection_pool_status()
    if "error" not in status:
        logger.info(
            f"Connection pool status: "
            f"{status['checked_out']}/{status['total_connections']} in use, "
            f"{status['checked_in']} available"
        )
    else:
        logger.warning(f"Pool status: {status['error']}")


def get_database_stats():
    """
    Get database statistics (table sizes, row counts, etc.).
    
    Returns:
        dict with database statistics
    """
    if engine is None:
        return {"error": "Database not configured"}
    
    stats = {}
    
    try:
        with SessionLocal() as session:
            from sqlalchemy import text
            
            # Get table sizes
            result = session.execute(text("""
                SELECT 
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
                    pg_total_relation_size(schemaname||'.'||tablename) AS size_bytes
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
            """))
            
            stats['tables'] = [
                {
                    'name': row[0],
                    'size': row[1],
                    'size_bytes': row[2]
                }
                for row in result
            ]
            
            # Get row counts
            from models import Conversation, Message, Usage
            
            stats['row_counts'] = {
                'conversations': session.query(Conversation).count(),
                'messages': session.query(Message).count(),
                'users': session.query(Usage).count()
            }
            
            # Get database size
            result = session.execute(text("""
                SELECT pg_size_pretty(pg_database_size(current_database()))
            """))
            stats['database_size'] = result.scalar()
            
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        stats['error'] = str(e)
    
    return stats


def log_database_stats():
    """Log database statistics."""
    stats = get_database_stats()
    
    if 'error' in stats:
        logger.error(f"Database stats error: {stats['error']}")
        return
    
    logger.info(f"Database size: {stats.get('database_size', 'unknown')}")
    logger.info(f"Row counts: {stats.get('row_counts', {})}")
    
    if 'tables' in stats:
        for table in stats['tables']:
            logger.info(f"  Table {table['name']}: {table['size']}")


# Example usage in endpoints
def monitor_query(query_name: str):
    """
    Context manager for monitoring database queries.
    
    Usage:
        with monitor_query("get_conversations"):
            # database operations
            pass
    """
    class QueryMonitor:
        def __init__(self, name):
            self.name = name
            self.start_time = None
        
        def __enter__(self):
            self.start_time = time.time()
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            duration = time.time() - self.start_time
            
            if exc_type is not None:
                logger.error(f"Query '{self.name}' failed after {duration:.2f}s: {exc_val}")
            elif duration > SLOW_QUERY_THRESHOLD:
                logger.warning(f"Slow query '{self.name}': {duration:.2f}s")
            else:
                logger.debug(f"Query '{self.name}' completed in {duration:.2f}s")
    
    return QueryMonitor(query_name)
