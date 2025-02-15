#!/bin/bash
PORT="$1"
echo " Starting LLM data enrichment service server with Uvicorn on port ${PORT}..."
uvicorn app.main:app --reload --port ${PORT} --log-level info