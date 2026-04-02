"""
YOLO Fruit Ninja - Python Backend Server
=========================================
FastAPI + YOLO + MPS Acceleration for Apple M3 Pro

This server handles:
1. Camera capture and YOLO object detection
2. WebSocket streaming of detection results to frontend
3. MPS-accelerated inference for real-time performance

Usage:
    python server.py
    
Author: Computer Vision Final Project
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import torch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="YOLO Fruit Ninja Backend",
    description="Real-time object detection server for Fruit Ninja game",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class YOLODetector:
    """
    YOLO26 Object Detector with MPS acceleration for Apple Silicon.
    
    YOLO26 Improvements over YOLO11:
    - End-to-End NMS-Free inference (faster, cleaner)
    - DFL (Distribution Focal Loss) removed (simpler export)
    - ProgLoss + STAL for better small-object detection
    - MuSGD Optimizer for stable training
    - Up to 43% faster CPU inference
    
    Supports:
    - YOLO26n/s/m/l/x variants
    - MPS (Metal Performance Shaders) acceleration
    - Real-time detection with configurable confidence thresholds
    """
    
    def __init__(
        self,
        model_path: str = "yolo26n.pt",
        confidence: float = 0.5,
        iou_threshold: float = 0.45,
        device: str = "mps",
        end2end: bool = True  # YOLO26 native end-to-end mode (no NMS)
    ):
        self.model_path = model_path
        self.confidence = confidence
        self.iou_threshold = iou_threshold
        self.preferred_device = device
        self.end2end = end2end  # True = no NMS (faster), False = with NMS (more accurate)
        
        # Load YOLO26 model
        logger.info(f"Loading YOLO26 model from: {model_path}")
        self.model = YOLO(model_path)
        
        # Set device (MPS for Apple Silicon)
        self._setup_device()
        
        # Class names for COCO dataset (common objects)
        # Fruits: apple(47), orange(58), banana(59), etc.
        self.fruit_classes = {
            47: "apple",
            48: "orange", 
            59: "banana",
            43: "cup",  # Can be used as fruit substitute
        }
        
        logger.info(f"✅ YOLO model loaded successfully on {self.device}")
    
    def _setup_device(self):
        """Configure computation device (MPS/CPU)"""
        if self.preferred_device == "mps" and torch.backends.mps.is_available():
            self.device = "mps"
            logger.info("🚀 Using MPS (Metal Performance Shaders) acceleration")
        elif torch.cuda.is_available():
            self.device = "cuda"
            logger.info("🚀 Using CUDA acceleration")
        else:
            self.device = "cpu"
            logger.info("⚠️  Using CPU (MPS/CUDA not available)")
        
        # Move model to device
        self.model.to(self.device)
    
    def detect(self, frame: np.ndarray) -> Dict:
        """
        Perform object detection on a frame using YOLO26.
        
        YOLO26 uses end-to-end inference without NMS by default.
        
        Args:
            frame: OpenCV BGR image frame
            
        Returns:
            Dictionary containing:
            - boxes: [[x1, y1, x2, y2, confidence, class_id], ...]
            - count: number of detections
            - fps: inference FPS
        """
        start_time = datetime.now()
        
        # Run inference with YOLO26 end-to-end mode (no NMS)
        results = self.model(
            frame,
            conf=self.confidence,
            iou=self.iou_threshold,
            device=self.device,
            verbose=False,
            end2end=self.end2end  # YOLO26 specific: True = no NMS
        )
        
        # Calculate FPS
        inference_time = (datetime.now() - start_time).total_seconds()
        fps = 1.0 / inference_time if inference_time > 0 else 0
        
        # Extract detection results
        detection_data = {
            "boxes": [],
            "count": 0,
            "fps": round(fps, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        if results[0].boxes is not None:
            boxes = results[0].boxes.data.cpu().numpy()
            detection_data["boxes"] = boxes.tolist()
            detection_data["count"] = len(boxes)
        
        return detection_data
    
    def get_detections_for_game(self, frame: np.ndarray) -> Dict:
        """
        Get detections formatted for the game frontend.
        
        Returns:
            Game-ready detection data with fruit/bomb classification
        """
        raw_detections = self.detect(frame)
        
        game_detections = {
            "fruits": [],
            "bombs": [],  # Could add bomb-like objects
            "hands": [],  # For gesture-based interaction
            "fps": raw_detections["fps"],
            "timestamp": raw_detections["timestamp"]
        }
        
        for box in raw_detections["boxes"]:
            x1, y1, x2, y2, conf, class_id = box
            class_id = int(class_id)
            
            detection = {
                "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                "confidence": float(conf),
                "class_id": class_id,
                "center": [float((x1 + x2) / 2), float((y1 + y2) / 2)]
            }
            
            # Classify for game logic
            if class_id in self.fruit_classes:
                game_detections["fruits"].append(detection)
            elif class_id == 0:  # person - could be hand/body
                game_detections["hands"].append(detection)
            else:
                # Other objects can be treated as fruits for demo
                game_detections["fruits"].append(detection)
        
        return game_detections


class CameraManager:
    """
    Manages camera capture and frame streaming.
    """
    
    def __init__(self, camera_id: int = 0, width: int = 640, height: int = 480):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
    
    def start(self) -> bool:
        """Initialize and start camera capture"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open camera {self.camera_id}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            logger.info(f"✅ Camera started: {self.width}x{self.height}@30fps")
            return True
            
        except Exception as e:
            logger.error(f"Camera start error: {e}")
            return False
    
    def read_frame(self) -> Optional[np.ndarray]:
        """Read a single frame from camera"""
        if not self.is_running or self.cap is None:
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        return frame
    
    def stop(self):
        """Stop camera capture"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            logger.info("📷 Camera stopped")


# Global instances
detector: Optional[YOLODetector] = None
camera: Optional[CameraManager] = None


@app.on_event("startup")
async def startup_event():
    """Initialize YOLO26 model and camera on startup"""
    global detector, camera
    
    logger.info("🚀 Starting YOLO26 Fruit Ninja Backend...")
    
    # Initialize YOLO26 detector
    # Use YOLO26n (nano) for real-time performance on M3 Pro
    # If yolo26n.pt is not available, it will auto-download from Ultralytics
    detector = YOLODetector(
        model_path="yolo26n.pt",  # YOLO26 nano variant (auto-downloads if missing)
        confidence=0.5,
        iou_threshold=0.45,
        device="mps",
        end2end=True  # YOLO26 native end-to-end (no NMS)
    )
    
    # Initialize camera
    camera = CameraManager(camera_id=0, width=640, height=480)
    
    if not camera.start():
        logger.warning("⚠️  Camera not available - will use fallback mode")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    global camera
    if camera:
        camera.stop()
    logger.info("👋 Server shutting down")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "YOLO Fruit Ninja Backend",
        "version": "1.0.0",
        "device": detector.device if detector else "not initialized",
        "model": detector.model_path if detector else "not loaded"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "yolo_model": detector.model_path if detector else "not loaded",
        "device": detector.device if detector else "not initialized",
        "camera": "connected" if camera and camera.is_running else "disconnected",
        "mps_available": torch.backends.mps.is_available(),
        "cuda_available": torch.cuda.is_available()
    }


@app.websocket("/ws/detect")
async def websocket_detect(websocket: WebSocket):
    """
    WebSocket endpoint for real-time object detection.
    
    Streams camera frames through YOLO and sends detection results.
    """
    await websocket.accept()
    
    if not camera or not camera.is_running:
        await websocket.send_json({
            "error": "Camera not available",
            "fallback": True
        })
        return
    
    logger.info("🔌 WebSocket client connected")
    
    try:
        while True:
            # Check if client is still connected
            try:
                # Non-blocking check for client messages
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=0.001
                )
                
                # Handle client commands
                msg = json.loads(data)
                if msg.get("type") == "stop":
                    logger.info("Client requested stop")
                    break
                    
            except asyncio.TimeoutError:
                pass
            except WebSocketDisconnect:
                logger.info("🔌 WebSocket client disconnected")
                return
            
            # Capture and process frame
            frame = camera.read_frame()
            
            if frame is not None and detector is not None:
                # Run detection
                detections = detector.get_detections_for_game(frame)
                
                # Send results to client
                await websocket.send_json(detections)
            else:
                # Send empty detection if no frame
                await websocket.send_json({
                    "fruits": [],
                    "bombs": [],
                    "hands": [],
                    "fps": 0,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Small delay to control FPS
            await asyncio.sleep(0.033)  # ~30 FPS
            
    except WebSocketDisconnect:
        logger.info("🔌 WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        logger.info("🔌 WebSocket connection closed")


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """
    WebSocket endpoint for video streaming + detection.
    
    Sends both the processed frame (as base64) and detection data.
    """
    await websocket.accept()
    
    if not camera or not camera.is_running:
        await websocket.send_json({"error": "Camera not available"})
        return
    
    logger.info("📹 WebSocket stream started")
    
    try:
        while True:
            frame = camera.read_frame()
            
            if frame is not None and detector is not None:
                # Run detection
                results = detector.model(
                    frame,
                    conf=detector.confidence,
                    device=detector.device,
                    verbose=False
                )
                
                # Draw detections on frame
                annotated_frame = results[0].plot()
                
                # Encode frame as JPEG
                _, buffer = cv2.imencode('.jpg', annotated_frame)
                frame_base64 = buffer.decode('utf-8')
                
                # Get detection data
                detections = detector.get_detections_for_game(frame)
                
                # Send both frame and data
                await websocket.send_json({
                    "type": "frame",
                    "frame": frame_base64,
                    "detections": detections
                })
            else:
                await asyncio.sleep(0.033)
                
    except WebSocketDisconnect:
        logger.info("📹 WebSocket stream disconnected")
    except Exception as e:
        logger.error(f"Stream error: {e}")


if __name__ == "__main__":
    import uvicorn
    
    logger.info("=" * 50)
    logger.info("🎮 YOLO26 Fruit Ninja Backend Server")
    logger.info("=" * 50)
    logger.info(f"📍 Model: yolo26n.pt (YOLO26 Nano)")
    logger.info(f"🚀 Features: End-to-End (No NMS), DFL Removed")
    logger.info(f"💻 Device: MPS (Apple M3 Pro)")
    logger.info(f"🌐 Server: http://localhost:8001")
    logger.info(f"🔌 WebSocket: ws://localhost:8001/ws/detect")
    logger.info("=" * 50)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
