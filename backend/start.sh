#!/bin/bash

echo "========================================"
echo "🚀 Starting NexGen Hospital API"
echo "========================================"

# -------------------------------
# Use Render PORT (IMPORTANT)
# -------------------------------
PORT=${PORT:-10000}
echo "🌐 Using PORT: $PORT"

# -------------------------------
# Install dependencies (Render safe)
# -------------------------------
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# -------------------------------
# Start FastAPI
# -------------------------------
echo "🔥 Launching server..."

exec uvicorn main:app --host 0.0.0.0 --port $PORT
