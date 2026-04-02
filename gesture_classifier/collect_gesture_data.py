"""
Gesture Data Collection Script
==============================
Captures hand landmark data from webcam using MediaPipe (new tasks API).
Records labeled gesture samples for training a gesture classifier.

Usage:
    python3 collect_gesture_data.py

Controls:
    1 - Record "slash" gesture (cutting motion)
    2 - Record "idle" gesture (hand visible, relaxed)
    3 - Record "grab" gesture (closed fist)
    4 - Record "open_palm" gesture (hand open, fingers spread)
    s - Save collected data to CSV
    q - Quit

Each keypress starts recording; any other key stops recording.
Aim for ~300-500 samples per gesture class.
"""

import cv2
import mediapipe as mp
import numpy as np
import csv
import os
import time

# Gesture labels
GESTURES = {
    "1": "slash",
    "2": "idle",
    "3": "grab",
    "4": "open_palm",
}

# MediaPipe new tasks API
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
BaseOptions = mp.tasks.BaseOptions
RunningMode = mp.tasks.vision.RunningMode


def extract_landmarks(hand_landmarks):
    """Extract normalized landmark features from hand landmarks.

    Returns 63 features: 21 landmarks x 3 coordinates (x, y, z).
    Coordinates are normalized relative to the wrist (landmark 0).
    """
    wrist = hand_landmarks[0]
    features = []
    for lm in hand_landmarks:
        features.extend([
            lm.x - wrist.x,
            lm.y - wrist.y,
            lm.z - wrist.z,
        ])
    return features


def draw_landmarks_on_frame(frame, hand_landmarks):
    """Draw hand landmarks and connections on the frame."""
    h, w = frame.shape[:2]
    # Draw landmarks as circles
    for lm in hand_landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

    # Draw connections (simplified - just connect sequential landmarks)
    connections = [
        (0,1),(1,2),(2,3),(3,4),       # thumb
        (0,5),(5,6),(6,7),(7,8),       # index
        (0,9),(9,10),(10,11),(11,12),   # middle
        (0,13),(13,14),(14,15),(15,16), # ring
        (0,17),(17,18),(18,19),(19,20), # pinky
        (5,9),(9,13),(13,17),           # palm
    ]
    for start, end in connections:
        if start < len(hand_landmarks) and end < len(hand_landmarks):
            x1, y1 = int(hand_landmarks[start].x * w), int(hand_landmarks[start].y * h)
            x2, y2 = int(hand_landmarks[end].x * w), int(hand_landmarks[end].y * h)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 200, 0), 2)


def main():
    data_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(data_dir, "gesture_data.csv")
    model_path = os.path.join(data_dir, "hand_landmarker.task")

    if not os.path.exists(model_path):
        print(f"ERROR: Model file not found at {model_path}")
        print("Download it: curl -sL -o hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
        return

    # Collected samples
    samples = []
    counts = {g: 0 for g in GESTURES.values()}

    # Load existing data if present
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                samples.append(row)
                label = row[-1]
                if label in counts:
                    counts[label] += 1
        print(f"Loaded {len(samples)} existing samples from {output_file}")

    # Create HandLandmarker
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )
    landmarker = HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    current_label = None
    recording = False
    prev_landmarks = None
    prev_time = None
    frame_timestamp = 0

    print("\n=== Gesture Data Collection ===")
    print("Press 1-4 to START recording a gesture class:")
    print("  1: slash (swipe/cut)    2: idle (hand relaxed)")
    print("  3: grab (closed fist)   4: open_palm (fingers spread)")
    print("Press any OTHER key to STOP recording")
    print("Press 's' to save, 'q' to quit")
    print(f"Current counts: {counts}\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        # Convert to MediaPipe Image
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        # Detect hand landmarks
        frame_timestamp += 33  # ~30fps
        results = landmarker.detect_for_video(mp_image, frame_timestamp)

        if results.hand_landmarks:
            hand_lms = results.hand_landmarks[0]  # first hand
            draw_landmarks_on_frame(frame, hand_lms)

            if recording and current_label:
                features = extract_landmarks(hand_lms)

                # Velocity features (reset if gap > 200ms to avoid stale data)
                now = time.time()
                stale = prev_time is not None and (now - prev_time) > 0.2
                if prev_landmarks is not None and prev_time is not None and not stale:
                    dt = now - prev_time
                    if dt > 0:
                        velocity = [(f - p) / dt for f, p in zip(features, prev_landmarks)]
                    else:
                        velocity = [0.0] * len(features)
                else:
                    velocity = [0.0] * len(features)

                prev_landmarks = features
                prev_time = now

                row = [str(v) for v in features + velocity] + [current_label]
                samples.append(row)
                counts[current_label] += 1

        # Display status
        if recording:
            status = f"RECORDING: {current_label}"
            color = (0, 0, 255)
            # Pulsing red circle indicator
            radius = 12 + int(5 * abs(np.sin(time.time() * 3)))
            cv2.circle(frame, (620, 30), radius, (0, 0, 255), -1)
        else:
            status = "Ready (press 1-4 to record)"
            color = (0, 255, 0)

        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        y_offset = 60
        for gesture, count in counts.items():
            bar_len = min(count // 3, 200)  # visual bar
            cv2.rectangle(frame, (130, y_offset - 12), (130 + bar_len, y_offset + 4), (100, 200, 100), -1)
            cv2.putText(frame, f"{gesture}: {count}", (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 25

        total = sum(counts.values())
        cv2.putText(frame, f"Total: {total}", (10, y_offset + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Gesture Data Collection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            save_data(samples, output_file)
            print(f"Saved {len(samples)} samples. Counts: {counts}")
        elif chr(key) in GESTURES if key < 128 else False:
            current_label = GESTURES[chr(key)]
            recording = True
            prev_landmarks = None
            prev_time = None
            print(f"Recording: {current_label}")
        elif key != 255:  # Any other key stops recording
            if recording:
                recording = False
                current_label = None
                prev_landmarks = None
                prev_time = None
                print("Stopped recording")

    # Auto-save on quit
    if samples:
        save_data(samples, output_file)
        print(f"\nAuto-saved {len(samples)} samples on exit. Counts: {counts}")

    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()


def save_data(samples, output_file):
    """Save collected samples to CSV."""
    n_landmarks = 21
    header = []
    for i in range(n_landmarks):
        header.extend([f"pos_x{i}", f"pos_y{i}", f"pos_z{i}"])
    for i in range(n_landmarks):
        header.extend([f"vel_x{i}", f"vel_y{i}", f"vel_z{i}"])
    header.append("label")

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(samples)


if __name__ == "__main__":
    main()
