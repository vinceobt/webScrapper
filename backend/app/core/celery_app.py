from celery import Celery
from celery.signals import worker_ready
import logging

logger = logging.getLogger(__name__)

celery_app = Celery('web_scraper',
                   include=['app.services.scraper'])  # Explicitly include the scraper module

# Load configuration from dedicated config module
celery_app.config_from_object('app.core.celery_config')

@worker_ready.connect
def at_start(sender, **kwargs):
    """Log when Celery worker is ready"""
    logger.info("Celery worker is ready")