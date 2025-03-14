import os
import sys
import logging
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.database import Base, engine
from app.models.models import ScrapingTask, ScrapingResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            logger.info("Database created successfully!")
        
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()