# Web Scraper Application

A full-stack web application for scraping websites and extracting content. This application follows a modern architecture with a React.js frontend and Python FastAPI backend, using Celery for asynchronous task processing.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Tech Stack](#tech-stack)
3. [Setup and Installation](#setup-and-installation)
4. [Running the Application](#running-the-application)
5. [API Documentation](#api-documentation)
6. [Features](#features)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

## Architecture Overview

The application follows this workflow:

1. **Frontend (React.js):** Users submit a URL through a form.
2. **Backend (FastAPI):** The URL is validated and a scraping task is created.
3. **Task Queue (Celery):** The scraping task is processed asynchronously.
4. **Scraper (Beautiful Soup/Requests):** Content is extracted from the website.
5. **Database (PostgreSQL):** Results are stored and made available to the frontend.
6. **Real-time Updates:** Frontend polls for status updates and displays results.

## Tech Stack

### Frontend
- React.js using Vite
- TypeScript
- Axios for API requests
- Modern CSS (custom styles)

### Backend
- FastAPI (Python)
- Celery for task queue
- Redis as message broker and result backend
- SQLAlchemy for ORM
- Beautiful Soup and Requests for web scraping
- PostgreSQL for data storage

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL database
- Redis server

### Backend Setup

1. Create and activate a virtual environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with the following configuration:
```
DATABASE_URL=postgresql://username:password@localhost/web_scraper
REDIS_HOST=localhost
REDIS_PORT=6379
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

4. Initialize the database:
```bash
python -m app.db.init_db
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

## Running the Application

### Start the Backend Services

1. Start the Redis server:
```bash
redis-server
```

2. Start the PostgreSQL database (if not already running):
```bash
# Command depends on your operating system and installation method
# On many systems, PostgreSQL is started as a service
```

3. Start the FastAPI server:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Start the Celery worker:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
celery -A app.core.celery_app worker --loglevel=info
```

### Start the Frontend

1. Start the React development server:
```bash
cd frontend
npm run dev
```

2. Open your browser and navigate to:
```
http://localhost:5173
```

## API Documentation

Once the application is running, you can access the FastAPI automatic documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

- `POST /api/scrape` - Submit a URL for scraping
- `GET /api/tasks/{task_id}` - Get a specific scraping task with results
- `GET /api/tasks` - List all scraping tasks
- `GET /api/task-status/{task_id}` - Get the status of a scraping task

## Features

- **URL Validation**: Ensures valid URLs are submitted
- **Asynchronous Processing**: Long-running scraping tasks don't block the main application
- **Real-time Status Updates**: Users can monitor the progress of their scraping tasks
- **Content Extraction**: Pulls out key information from web pages:
  - Title and meta description
  - Links
  - Images
- **Responsive UI**: Works across desktop and mobile devices
- **Rate Limiting**: Built-in mechanisms to avoid overloading target websites

## Deployment

### Production Considerations

For production deployment, consider:

1. Using Gunicorn as the WSGI server for FastAPI
2. Setting up load balancing with multiple Celery workers
3. Adding authentication and rate limiting for API endpoints
4. Using a managed PostgreSQL service
5. Using a managed Redis service or deploying Redis Cluster
6. Building the React frontend for production and serving with Nginx

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check that PostgreSQL is running and the connection string is correct
   - Ensure the database exists and has the correct permissions

2. **Redis Connection Errors**
   - Verify Redis is running on the configured host and port
   - Check that Redis is not protected by password or is configured correctly

3. **Celery Worker Not Processing Tasks**
   - Ensure the Celery worker is running and connected to Redis
   - Check logs for any error messages

4. **Scraping Issues**
   - Some websites may block scraping attempts
   - Try using different user-agent headers or proxy settings

5. **CORS Issues**
   - Verify that the backend is configured to accept requests from the frontend origin