import random
import time
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from urllib.parse import urljoin, urlparse

from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.database import SessionLocal
from app.models.models import ScrapingTask, ScrapingResult, TaskStatus

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def normalize_url(base_url: str, url: str) -> str:
    """Convert relative URLs to absolute URLs"""
    try:
        return urljoin(base_url, url)
    except Exception:
        return url

@celery_app.task(name="scrape_url", bind=True, max_retries=3)
def scrape_url(self, task_id: int) -> Dict[str, Any]:
    """
    Celery task for scraping a URL.
    Updates task status and saves the scraped data.
    """
    db = SessionLocal()
    try:
        # Get the task from the database
        task = db.query(ScrapingTask).filter(ScrapingTask.id == task_id).first()
        if not task:
            logger.error(f"Task with ID {task_id} not found")
            return {"error": f"Task with ID {task_id} not found"}
        
        # Update task status to in progress
        task.status = TaskStatus.IN_PROGRESS.value
        db.commit()
        
        # Validate URL
        if not is_valid_url(str(task.url)):
            raise ValueError("Invalid URL format")
        
        # Perform the scraping with delay to respect rate limits
        try:
            # Random delay to prevent rate limiting
            time.sleep(random.uniform(1, settings.SCRAPER_DELAY))
            
            # Request with rotating user agent
            user_agent = random.choice(settings.USER_AGENTS)
            headers = {
                "User-Agent": user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
            
            response = requests.get(
                str(task.url), 
                headers=headers, 
                timeout=30,
                verify=True
            )
            response.raise_for_status()
            
            # Process with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract metadata
            title = soup.title.string if soup.title else ""
            meta_description = ""
            meta_desc_tag = soup.find("meta", attrs={"name": "description"}) or \
                           soup.find("meta", attrs={"property": "og:description"})
            if meta_desc_tag and meta_desc_tag.get("content"):
                meta_description = meta_desc_tag.get("content")
            
            # Extract and normalize links
            links = []
            for a in soup.find_all('a', href=True):
                href = a.get('href')
                if href and not href.startswith(('javascript:', 'mailto:', 'tel:')):
                    normalized_url = normalize_url(str(task.url), href)
                    if is_valid_url(normalized_url):
                        links.append(normalized_url)
            
            # Extract and normalize images
            images = []
            for img in soup.find_all('img', src=True):
                src = img.get('src')
                if src:
                    normalized_url = normalize_url(str(task.url), src)
                    if is_valid_url(normalized_url):
                        images.append(normalized_url)
            
            # Store the result
            result = ScrapingResult(
                task_id=task.id,
                content={
                    "title": title,
                    "meta_description": meta_description,
                    "url": str(task.url),
                    "links_count": len(links),
                    "images_count": len(images),
                    "links": links[:100],  # Limit to first 100 links
                    "images": images[:50],  # Limit to first 50 images
                },
                html_content=response.text[:100000]  # Store first 100K chars of HTML
            )
            
            db.add(result)
            
            # Update task status to completed
            task.status = TaskStatus.COMPLETED.value
            task.completed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Successfully scraped {task.url} for task {task_id}")
            return {
                "status": "success",
                "task_id": task_id,
                "result_id": result.id
            }
            
        except requests.RequestException as e:
            logger.error(f"Request error for URL {task.url}: {str(e)}")
            task.status = TaskStatus.FAILED.value
            task.error_message = f"Failed to fetch URL: {str(e)}"
            db.commit()
            
            # Retry for certain status codes
            if hasattr(e.response, 'status_code') and e.response.status_code in [429, 503]:
                raise self.retry(exc=e, countdown=60)  # Retry after 1 minute
                
            return {"status": "failed", "task_id": task_id, "error": str(e)}
            
        except Exception as e:
            logger.error(f"Error scraping URL {task.url}: {str(e)}")
            task.status = TaskStatus.FAILED.value
            task.error_message = str(e)
            db.commit()
            return {"status": "failed", "task_id": task_id, "error": str(e)}
    
    finally:
        db.close()

def create_scraping_task(db: Session, url: str) -> ScrapingTask:
    """Create a new scraping task in the database."""
    if not is_valid_url(url):
        raise ValueError("Invalid URL format")
        
    task = ScrapingTask(url=url, status=TaskStatus.PENDING.value)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task_by_id(db: Session, task_id: int) -> Optional[ScrapingTask]:
    """Get a scraping task by ID."""
    return db.query(ScrapingTask).filter(ScrapingTask.id == task_id).first()

def get_task_with_results(db: Session, task_id: int) -> Optional[ScrapingTask]:
    """Get a scraping task with its results."""
    return db.query(ScrapingTask).filter(ScrapingTask.id == task_id).first()