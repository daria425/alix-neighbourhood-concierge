#!/bin/bash


if [ -z "$1" ]; then
  echo "What port love 😕"
  exit 1
fi
PORT="$1"
echo "🌟 Starting Chatbot FastAPI server with Uvicorn on port ${PORT}... 🌟"
uvicorn app.main:app --host 127.0.0.1 --reload --port ${PORT} --log-level info
