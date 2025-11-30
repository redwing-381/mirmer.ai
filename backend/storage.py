"""
Storage factory - automatically selects PostgreSQL or JSON backend.
"""
import os
import logging

logger = logging.getLogger(__name__)

# Determine which storage backend to use
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    logger.info("✓ Using PostgreSQL storage backend (production)")
    from storage_postgres import *
else:
    logger.info("✓ Using JSON file storage backend (local development)")
    from storage_json import *
