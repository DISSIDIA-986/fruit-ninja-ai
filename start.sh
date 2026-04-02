#!/bin/bash

echo "🚀 Starting Fruit Ninja Game Servers..."
echo "========================================"

# Activate virtual environment
source venv/bin/activate

# Start backend server in background
echo "📦 Starting YOLO26 Backend on http://localhost:8001"
python3 server.py &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 5

# Start frontend server
echo "🎨 Starting Vite Frontend on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "========================================"
echo "✅ Servers are running!"
echo "   - YOLO26 Mode: http://localhost:3000/index-yolo.html"
echo "   - MediaPipe Mode: http://localhost:3000/index.html"
echo "   - Backend API: http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "========================================"

# Open browser
sleep 3
open http://localhost:3000/index-yolo.html
open http://localhost:3000/index.html

# Wait for processes
wait
