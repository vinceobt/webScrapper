from sqlalchemy.orm import Session
from app.db.database import Base, engine
from app.models.models import ScrapingTask, ScrapingResult
import logging

logger = logging.getLogger(__name__)

def init_db() -> None:
    """Initialize the database by creating all tables."""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!")