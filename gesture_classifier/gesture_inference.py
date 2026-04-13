"""
Gesture Inference Module
========================
Loads the trained gesture classifier and provides real-time gesture prediction
from MediaPipe hand landmarks. Uses the new MediaPipe tasks API.

Usage (standalone demo):
    python3 gesture_inference.py
"""

import cv2
import mediapipe as mp
import numpy as np
import torch
import torch.nn as nn
import joblib
import os
import time

# MediaPipe new tasks API
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
BaseOptions = mp.tasks.BaseOptions
RunningMode = mp.tasks.vision.RunningMode


class GestureClassifier(nn.Module):
    """MLP classifier for hand gesture recognition."""

    def __init__(self, input_size, num_classes, dropout=0.3):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes),
        )

    def forward(self, x):
        return self.network(x)


class GesturePredictor:
    """Real-time gesture prediction from webcam using MediaPipe + trained MLP."""

    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = os.path.dirname(os.path.abspath(__file__))

        model_path = os.path.join(model_dir, "gesture_model.pth")
        scaler_path = os.path.join(model_dir, "gesture_scaler.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at {model_path}. Run the training notebook first."
            )

        checkpoint = torch.load(model_path, map_location="cpu", weights_only=True)
        self.class_names = checkpoint["class_names"]
        self.model = GestureClassifier(
            checkpoint["input_size"], checkpoint["num_classes"]
        )
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

        self.scaler = joblib.load(scaler_path)

        self.prev_landmarks = None
        self.prev_time = None

        print(f"Gesture model loaded. Classes: {self.class_names}")
        print(f"Test accuracy: {checkpoint.get('test_accuracy', 'N/A')}")

    def extract_features(self, hand_landmarks):
        """Extract position + velocity features from hand landmarks."""
        wrist = hand_landmarks[0]
        positions = []
        for lm in hand_landmarks:
            positions.extend([lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z])

        now = time.time()
        stale = self.prev_time is not None and (now - self.prev_time) > 0.2
        if self.prev_landmarks is not None and self.prev_time is not None and not stale:
            dt = now - self.prev_time
            if dt > 0:
                velocity = [(p - prev) / dt for p, prev in zip(positions, self.prev_landmarks)]
            else:
                velocity = [0.0] * len(positions)
        else:
            velocity = [0.0] * len(positions)

        self.prev_landmarks = positions
        self.prev_time = now
        return positions + velocity

    def predict(self, hand_landmarks):
        """Predict gesture from hand landmarks. Returns (gesture_name, confidence)."""
        features = self.extract_features(hand_landmarks)
        features_scaled = self.scaler.transform([features])
        inputs = torch.tensor(features_scaled, dtype=torch.float32)

        with torch.no_grad():
            outputs = self.model(inputs)
            probs = torch.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probs, 1)

        gesture = self.class_names[predicted.item()]
        return gesture, confidence.item()


def draw_landmarks(frame, hand_landmarks):
    """Draw hand landmarks on frame."""
    h, w = frame.shape[:2]
    connections = [
        (0,1),(1,2),(2,3),(3,4),
        (0,5),(5,6),(6,7),(7,8),
        (0,9),(9,10),(10,11),(11,12),
        (0,13),(13,14),(14,15),(15,16),
        (0,17),(17,18),(18,19),(19,20),
        (5,9),(9,13),(13,17),
    ]
    for s, e in connections:
        if s < len(hand_landmarks) and e < len(hand_landmarks):
            x1, y1 = int(hand_landmarks[s].x * w), int(hand_landmarks[s].y * h)
            x2, y2 = int(hand_landmarks[e].x * w), int(hand_landmarks[e].y * h)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 200, 0), 2)
    for lm in hand_landmarks:
        cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 4, (0, 255, 0), -1)


def main():
    """Standalone demo: real-time gesture classification from webcam."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    predictor = GesturePredictor(script_dir)

    model_path = os.path.join(script_dir, "hand_landmarker.task")
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )
    landmarker = HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    gesture_colors = {
        "slash": (0, 0, 255),
        "idle": (0, 255, 0),
        "grab": (255, 165, 0),
        "open_palm": (255, 255, 0),
    }

    fps_start = time.time()
    frame_count = 0
    fps = 0
    frame_timestamp = 0

    print("\nReal-time gesture classification running. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        frame_timestamp += 33
        results = landmarker.detect_for_video(mp_image, frame_timestamp)

        gesture = "No hand"
        confidence = 0.0

        if results.hand_landmarks:
            hand_lms = results.hand_landmarks[0]
            draw_landmarks(frame, hand_lms)
            gesture, confidence = predictor.predict(hand_lms)

        color = gesture_colors.get(gesture, (255, 255, 255))
        cv2.putText(frame, f"{gesture} ({confidence:.0%})", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        frame_count += 1
        elapsed = time.time() - fps_start
        if elapsed > 1.0:
            fps = frame_count / elapsed
            frame_count = 0
            fps_start = time.time()
        cv2.putText(frame, f"FPS: {fps:.0f}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        cv2.imshow("Gesture Classifier Demo", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()


if __name__ == "__main__":
    main()
