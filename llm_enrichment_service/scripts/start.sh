#!/bin/bash
PORT="$1"
echo "Starting FastAPI server with Uvicorn on port ${PORT}..."
uvicorn app.main:app --reload --port ${PORT} --log-level info