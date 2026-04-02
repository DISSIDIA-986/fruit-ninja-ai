#!/bin/bash
# YOLO26 Fruit Ninja - Quick Start Script
# Usage: ./run.sh

set -e

echo "=================================================="
echo "🍉 YOLO26 Fruit Ninja - Starting..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📥 Checking dependencies..."
pip3 install -q -r requirements.txt 2>/dev/null || true

# Check Node.js dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

echo ""
echo "=================================================="
echo "🚀 Starting YOLO Fruit Ninja"
echo "=================================================="
echo ""
echo "📍 Backend Server: http://localhost:8000"
echo "📍 Frontend: http://localhost:5173"
echo "📍 Game URL: http://localhost:5173/index-yolo.html"
echo ""
echo "=================================================="
echo ""

# Start backend server in background
echo "🐍 Starting Python backend..."
python3 server.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend dev server
echo "🌐 Starting frontend dev server..."
npm run dev

# Cleanup on exit
trap "kill $BACKEND_PID 2>/dev/null || true" EXIT
