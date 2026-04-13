# 🍉 YOLO26 Fruit Ninja - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd esa-project02

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip3 install -r requirements.txt
```

### Step 2: Verify MPS Acceleration

```bash
# Test MPS availability
python3 -c "import torch; print('MPS:', torch.backends.mps.is_available())"

# Expected output: MPS: True
```

### Step 3: Start Backend Server

```bash
# Terminal 1
python3 server.py
```

Expected output:
```
🚀 Starting YOLO Fruit Ninja Backend...
🔍 Loading YOLO model from: yolo11n.pt
🚀 Using MPS (Metal Performance Shaders) acceleration
✅ YOLO model loaded successfully on mps:0
🌐 Server: http://localhost:8000
```

### Step 4: Start Frontend

```bash
# Terminal 2 (new terminal)
npm install
npm run dev
```

Expected output:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Step 5: Open Browser

Navigate to: **http://localhost:5173/index-yolo.html**

---

## 🎮 How to Play

1. **Click "START GAME"** to begin
2. **Mouse/Touch** to cut the detected fruits
3. **Avoid bombs** (black spheres)
4. **SPACE** to pause/resume
5. **M** to toggle YOLO/Fallback mode
6. **P** to show performance monitor

---

## 🧪 Run Tests

### Test MPS Performance

```bash
python3 tests/benchmark_mps.py
```

Expected output:
```
🔍 Device Check
PyTorch Version: 2.x.x
MPS Available: True
✅ Using MPS (Metal Performance Shaders)

🚀 Running Benchmark
   Iterations: 100
   Image Size: 640x640
   Device: mps

📊 Results
   Average: 15.23 ms
   FPS: 65.7

📈 Performance Rating: 🟢 Excellent - Ready for real-time gameplay
```

### Test Camera

```bash
python3 tests/test_camera.py
```

---

## 🐛 Troubleshooting

### Issue: "MPS not available"

```bash
# Reinstall PyTorch
pip3 uninstall torch torchvision
pip3 install torch torchvision
```

### Issue: "Port 8000 already in use"

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python3 server.py --port 8001
```

### Issue: "Camera not found"

- Check camera permissions: System Preferences > Security & Privacy > Privacy > Camera
- Try external camera if built-in not working
- Use fallback mode (M key) if camera unavailable

---

## 📊 Performance Expectations

| Hardware | Expected FPS |
|----------|-------------|
| **M3 Pro (this project)** | 60-80 FPS |
| M1/M2 | 50-70 FPS |
| Intel Mac | 15-25 FPS |
| Windows (GTX 1060) | 40-60 FPS |

---

## 🎯 Next Steps

1. **Read Full Report**: See `YOLO_PROJECT_REPORT.md`
2. **Understand Architecture**: Check `server.py` comments
3. **Customize Game**: Edit `src/index-yolo.js`
4. **Deploy to ESA**: See `DEPLOYMENT.md`

---

## 📚 Project Files

| File | Purpose |
|------|---------|
| `server.py` | Python backend (YOLO + FastAPI) |
| `index-yolo.html` | Game UI |
| `src/index-yolo.js` | Frontend logic |
| `src/components/YOLODetector.js` | WebSocket YOLO client |
| `requirements.txt` | Python dependencies |
| `tests/benchmark_mps.py` | Performance test |

---

**Enjoy the game! 🎮**
