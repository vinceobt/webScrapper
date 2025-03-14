from app.core.config import settings

broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND

# Celery Configuration
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

# Task settings
worker_prefetch_multiplier = 1
task_acks_late = True
task_reject_on_worker_lost = True
task_routes = {
    'scrape_url': {'queue': 'scraping'}
}

# Time limits
task_time_limit = 300  # 5 minutes max per task
task_soft_time_limit = 240  # Soft limit of 4 minutes

# Broker settings
broker_connection_retry_on_startup = True
broker_connection_max_retries = None

# Result settings
result_expires = 60 * 60 * 24  # Results expire after 24 hours

# List of modules to import when the Celery worker starts
imports = ('app.services.scraper',)