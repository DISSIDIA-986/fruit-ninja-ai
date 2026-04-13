"""
Camera Test Script for YOLO26 Fruit Ninja
========================================

Tests camera availability and capture functionality.

Usage:
    python3 tests/test_camera.py
"""

import cv2
import numpy as np

def test_camera(camera_id=0, width=640, height=480):
    """Test camera capture"""
    print("=" * 50)
    print("📷 Camera Test")
    print("=" * 50)
    
    print(f"\n🔍 Testing Camera {camera_id}...")
    print(f"   Resolution: {width}x{height}")
    
    # Open camera
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"❌ Failed to open camera {camera_id}")
        return False
    
    # Check properties
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"✅ Camera opened successfully")
    print(f"   Actual Resolution: {actual_width}x{actual_height}")
    print(f"   FPS: {fps}")
    
    # Set properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Capture frames
    print(f"\n🎬 Capturing test frames...")
    
    frame_count = 0
    success_count = 0
    
    while frame_count < 30:
        ret, frame = cap.read()
        
        if ret:
            success_count += 1
            
            # Show frame (optional)
            if frame_count == 0:
                print(f"   Frame shape: {frame.shape}")
                print(f"   Frame dtype: {frame.dtype}")
        else:
            print(f"   ⚠️  Frame {frame_count} failed")
        
        frame_count += 1
    
    # Release camera
    cap.release()
    
    # Results
    success_rate = (success_count / frame_count) * 100
    
    print(f"\n📊 Test Results")
    print(f"   Frames Captured: {frame_count}")
    print(f"   Successful: {success_count}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print(f"\n✅ Camera test PASSED")
        return True
    else:
        print(f"\n❌ Camera test FAILED")
        return False


def list_cameras():
    """List available cameras"""
    print("\n📹 Available Cameras:")
    
    # Test first 5 camera IDs
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"   ✅ Camera {i}: Available")
            cap.release()
        else:
            print(f"   ❌ Camera {i}: Not available")


def main():
    """Main test function"""
    print("\n" + "=" * 50)
    print("🎮 YOLO26 Fruit Ninja - Camera Test")
    print("=" * 50)
    
    # List available cameras
    list_cameras()
    
    # Test default camera
    result = test_camera(camera_id=0)
    
    print("\n" + "=" * 50)
    print("✅ Test Complete")
    print("=" * 50)
    
    return result


if __name__ == "__main__":
    main()
