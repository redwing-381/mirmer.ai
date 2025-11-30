"""
Usage factory - automatically selects PostgreSQL or JSON backend.
"""
import os
import logging

logger = logging.getLogger(__name__)

# Determine which usage backend to use
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    logger.info("✓ Using PostgreSQL usage tracking (production)")
    from backend.usage_postgres import *
else:
    logger.info("✓ Using JSON file usage tracking (local development)")
    from backend.usage_json import *
