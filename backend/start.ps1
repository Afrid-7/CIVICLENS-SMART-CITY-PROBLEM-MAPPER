# CivicLens Backend Startup Script
# Run this to start the backend server

cd D:\civiclens-frontend\backend
& D:\civiclens-frontend\backend\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
