#!/bin/bash
PORT="$1"
echo "Starting FastAPI server with Uvicorn on port ${PORT}..."
uvicorn app.main:app --host 127.0.0.1 --reload --port ${PORT}
