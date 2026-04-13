# Fruit Ninja - AI Gesture-Controlled Game

## Slide 1: Title

Fruit Ninja - AI Gesture-Controlled Game
Real-time Hand Tracking with MediaPipe & Three.js
Group 9 | Introduction to Computer Vision | SAIT Integrated AI Program

## Slide 2: Problem Statement

### The Problem
- Traditional gaming relies on controllers, keyboards, or touchscreens
- These input devices create a barrier between the player and the game
- Gesture-based interaction is more natural but technically challenging
- Existing gesture games require expensive hardware (Kinect, Leap Motion)

### Our Goal
- Build a gesture-controlled fruit-cutting game using only a webcam
- No special hardware required, runs in any modern browser
- Real-time hand tracking at 60 FPS with sub-16ms latency
- Deployed and accessible via web (Aliyun ESA)

## Slide 3: Challenges & Solutions

! Accurate hand detection in varied lighting conditions
+ MediaPipe Hand Landmarker with adaptive brightness optimization
! Distinguishing gestures: slash vs. idle vs. grab
+ Custom MLP classifier trained on 21 hand landmarks (126 features)
! Achieving real-time performance across different devices
+ Device-adaptive performance system with 3 quality presets
! Overlaying 3D game graphics on live camera feed
+ Three.js transparent rendering layered over webcam video
! Deploying to production with HTTPS camera access
+ Aliyun ESA deployment with CDN fallback for model loading

## Slide 4: System Architecture

### Input Layer
- Webcam captures video at 30-60 FPS
- MediaPipe HandLandmarker extracts 21 3D landmarks per hand
- Supports dual-hand tracking simultaneously

### Processing Layer
- GestureClassifier: MLP neural network (126 features, 4 classes)
- Feature extraction: position (63) + velocity (63) relative to wrist
- TrailRenderer: Fluorescent neon trail effects on 2D canvas

### Rendering Layer
- Three.js 3D scene with PerspectiveCamera
- Fruit physics: parabolic trajectories with gravity
- Particle explosion system for cutting effects
- ScoreSystem: +10 per fruit, -20 per bomb, 60s timer

## Slide 5: Hand Tracking - MediaPipe

### MediaPipe Hand Landmarker
- Google's state-of-the-art hand tracking solution
- Detects 21 3D landmarks per hand in real-time
- Uses @mediapipe/tasks-vision v0.10.22
- Runs entirely in the browser (no server needed for tracking)

### Our Optimizations
- Prediction-based hand smoothing (3-frame history buffer)
- Trail retention: 150ms with 15-point maximum length
- Adaptive detection interval: 16ms (60fps) on high-end, 33ms (30fps) on low-end
- Multiple CDN fallback sources for model loading reliability

### Performance Results

| Device Tier | Detection FPS | Particle Count | Target FPS |
|-------------|---------------|----------------|------------|
| Low-end | 30 fps | 15 | 30 fps |
| Medium | 45 fps | 25 | 60 fps |
| High-end | 60 fps | 30 | 60 fps |

## Slide 6: Gesture Classification - ML Pipeline

### Data Collection
- Custom data collection script (collect_gesture_data.py)
- Captures MediaPipe landmarks with labeled gestures
- 4 gesture classes: slash, idle, grab, open_palm

### Feature Engineering (126 dimensions)
- 63 position features: each landmark (x,y,z) relative to wrist
- 63 velocity features: frame-to-frame displacement / delta time
- StandardScaler normalization for consistent input ranges

### Model Architecture
- Multi-Layer Perceptron (MLP) trained in PyTorch
- Exported weights to JSON for browser-side inference
- No Python server needed: pure JavaScript forward pass
- Real-time classification with high accuracy

## Slide 7: Visual Effects & Game Engine

### Three.js 3D Rendering
- Transparent WebGL canvas layered over live camera feed
- 5 fruit types: apple, watermelon, orange, banana, pineapple
- Bomb objects with penalty scoring (-20 points)
- Progressive difficulty: spawn rate increases over game time

### Fluorescent Trail Effects
- Neon Blue (#00FFFF) for left hand
- Neon Green (#00FF00) for right hand
- Hot Pink (#FF1493) for mouse/touch fallback
- Canvas 2D rendering with glow and fade effects

### Collision Detection
- 3D ray-based cutting path intersection
- Hand trail points mapped from screen to 3D world coordinates
- Real-time particle explosion on successful cuts

## Slide 8: Live Demo

- Live demonstration of the Fruit Ninja game
- Hand gesture controls with webcam
- Dual-hand tracking and fluorescent trail effects
- Score tracking and difficulty progression
- Fallback to mouse control if camera unavailable

## Slide 9: Team Contributions

| Member | Responsibilities |
|--------|-----------------|
| Niu, Jason | Hand tracking integration (MediaPipe), gesture classifier ML pipeline, performance optimization, deployment (Aliyun ESA) |
| Si, Jack | Three.js game engine, fruit physics & collision detection, visual effects (trails, particles), UI/UX design |
| Bustamante Perez, Angel Daniel | Data collection for gesture training, testing & QA across devices, documentation |
| Lemes Cordeiro, Romilson | YOLO26 object detection integration, Python backend (FastAPI + WebSocket), benchmark testing |

## Slide 10: Results & Lessons Learned

### Results
- 60 FPS hand tracking on modern devices with <16ms latency
- Gesture classifier achieves high accuracy on 4 gesture classes
- YOLO26 alternative: 134 FPS on M3 Pro (7.4ms per frame)
- Successfully deployed on Aliyun ESA with global CDN access

### Lessons Learned
- MediaPipe runs entirely client-side, eliminating server round-trip latency
- Hand smoothing (3-frame buffer) dramatically reduces false gesture triggers
- Device-adaptive presets are essential for cross-device compatibility
- HTTPS is mandatory for camera access in production environments

### Future Work
- Add more gesture types (pinch zoom, rotate)
- Multiplayer mode with split-screen
- Mobile-optimized version with touch gesture training
