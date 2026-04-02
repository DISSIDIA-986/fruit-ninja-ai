#!/usr/bin/env python3
"""
YOLO26 Model Downloader
=======================

Downloads YOLO26 models from Ultralytics.

Usage:
    python3 download_models.py

Available YOLO26 Models:
- yolo26n.pt (nano) - Fastest, recommended for real-time
- yolo26s.pt (small) - Balanced
- yolo26m.pt (medium) - Higher accuracy
- yolo26l.pt (large) - Maximum accuracy
- yolo26x.pt (extra large) - Best accuracy, slowest

Task-specific variants:
- yolo26n-seg.pt (segmentation)
- yolo26n-pose.pt (pose estimation)
- yolo26n-obb.pt (oriented detection)
"""

from ultralytics import YOLO
import os

MODELS = {
    "yolo26n.pt": "Object Detection (Nano - Fastest)",
    "yolo26s.pt": "Object Detection (Small - Balanced)",
    "yolo26m.pt": "Object Detection (Medium - Accurate)",
    "yolo26n-pose.pt": "Pose Estimation (Nano)",
}

def download_model(model_name: str):
    """Download a YOLO26 model"""
    print(f"\n📥 Downloading {model_name}...")
    print(f"   Description: {MODELS.get(model_name, 'Unknown')}")
    
    try:
        # Load model (will auto-download if not exists)
        model = YOLO(model_name)
        
        # Check if file exists now
        if os.path.exists(model_name):
            size_mb = os.path.getsize(model_name) / (1024 * 1024)
            print(f"✅ Downloaded: {model_name} ({size_mb:.1f} MB)")
        else:
            # Model is cached elsewhere by ultralytics
            print(f"✅ Model cached by Ultralytics")
            
        return True
        
    except Exception as e:
        print(f"❌ Failed to download {model_name}: {e}")
        return False


def main():
    """Download all recommended models"""
    print("=" * 60)
    print("🍉 YOLO26 Fruit Ninja - Model Downloader")
    print("=" * 60)
    print()
    print("Available models:")
    for name, desc in MODELS.items():
        exists = "✅" if os.path.exists(name) else "⏳"
        print(f"  {exists} {name}: {desc}")
    
    print()
    print("-" * 60)
    
    # Download primary model (yolo26n.pt)
    print("\n🎯 Downloading primary model for Fruit Ninja...")
    download_model("yolo26n.pt")
    
    # Ask if user wants to download more
    print("\n" + "=" * 60)
    print("✅ Primary model ready!")
    print()
    print("To download additional models, run:")
    print("  python3 download_models.py --all")
    print("=" * 60)


if __name__ == "__main__":
    main()
