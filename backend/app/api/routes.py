from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas import schemas
from app.services.scraper import create_scraping_task, get_task_by_id, get_task_with_results, scrape_url
from app.core.celery_app import celery_app
from app.models.models import ScrapingTask

api_router = APIRouter()

@api_router.post("/scrape", response_model=schemas.ScrapingTaskResponse)
async def create_scrape_task(
    task_in: schemas.ScrapingTaskCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new web scraping task and queue it for processing.
    """
    # Create task in database
    task = create_scraping_task(db=db, url=str(task_in.url))
    
    # Queue task with Celery
    celery_app.send_task("scrape_url", args=[task.id])
    
    return task

@api_router.get("/tasks/{task_id}", response_model=schemas.TaskWithResults)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a web scraping task by ID, including results if available.
    """
    task = get_task_with_results(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@api_router.get("/tasks", response_model=List[schemas.ScrapingTaskResponse])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all web scraping tasks.
    """
    tasks = db.query(ScrapingTask).offset(skip).limit(limit).all()
    return tasks

@api_router.get("/task-status/{task_id}")
async def get_task_status(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the status of a web scraping task.
    """
    task = get_task_by_id(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": task.id,
        "status": task.status,
        "created_at": task.created_at,
        "completed_at": task.completed_at,
        "error_message": task.error_message
    }