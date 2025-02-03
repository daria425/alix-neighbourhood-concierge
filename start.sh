#!/bin/bash
echo "Starting FastAPI server with Uvicorn..."
uvicorn app.main:app --reload
