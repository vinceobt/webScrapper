#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Checking requirements..."

# Check Python
if ! command_exists python3; then
    echo "Python 3 is not installed. Please install Python 3."
    exit 1
fi

# Check Node.js
if ! command_exists node; then
    echo "Node.js is not installed. Please install Node.js."
    exit 1
fi

# Check Redis
if ! command_exists redis-cli; then
    echo "Redis is not installed. Please install Redis."
    exit 1
fi

# Check PostgreSQL
if ! command_exists psql; then
    echo "PostgreSQL is not installed. Please install PostgreSQL."
    exit 1
fi

echo "Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python db_init.py

echo "Starting Redis (if not already running)..."
if ! redis-cli ping > /dev/null 2>&1; then
    redis-server &
    sleep 2
fi

echo "Starting Celery worker..."
celery -A app.core.celery_app worker --loglevel=info &

echo "Starting FastAPI backend..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

echo "Installing frontend dependencies..."
cd ../frontend
npm install

echo "Starting frontend development server..."
npm run dev &

echo "All services have been started!"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"

# Keep the script running
wait