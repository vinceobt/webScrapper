from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import enum

Base = declarative_base()

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ScrapingTask(Base):
    __tablename__ = "scraping_tasks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1024), nullable=False)
    status = Column(String(20), default=TaskStatus.PENDING.value)  # Fixed: Use .value for enum
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationship to results (one-to-many)
    results = relationship("ScrapingResult", back_populates="task", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ScrapingTask(id={self.id}, url={self.url}, status={self.status})>"

class ScrapingResult(Base):
    __tablename__ = "scraping_results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("scraping_tasks.id"))
    content = Column(JSON, nullable=True)
    html_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to task (many-to-one)
    task = relationship("ScrapingTask", back_populates="results")
    
    def __repr__(self):
        return f"<ScrapingResult(id={self.id}, task_id={self.task_id})>"