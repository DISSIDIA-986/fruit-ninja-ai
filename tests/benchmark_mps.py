"""
MPS Acceleration Benchmark for YOLO26 Fruit Ninja
================================================

Tests YOLO26 inference performance on Apple M3 Pro with MPS acceleration.

YOLO26 Advantages:
- End-to-End inference without NMS
- DFL removed for simpler export
- ProgLoss + STAL for better small-object detection
- MuSGD Optimizer for stable training
- Up to 43% faster CPU inference vs YOLO11

Usage:
    python3 tests/benchmark_mps.py
"""

import time
import numpy as np
from ultralytics import YOLO
import torch

def check_device():
    """Check available computation devices"""
    print("=" * 50)
    print("🔍 Device Check")
    print("=" * 50)
    
    print(f"PyTorch Version: {torch.__version__}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    print(f"MPS Available: {torch.backends.mps.is_available()}")
    print(f"MPS Built: {torch.backends.mps.is_built()}")
    
    if torch.backends.mps.is_available():
        device = "mps"
        print("✅ Using MPS (Metal Performance Shaders)")
    elif torch.cuda.is_available():
        device = "cuda"
        print("✅ Using CUDA")
    else:
        device = "cpu"
        print("⚠️  Using CPU (no GPU acceleration)")
    
    return device


def load_model(model_path="yolo26n.pt"):
    """Load YOLO26 model"""
    print(f"\n📥 Loading model: {model_path}")
    model = YOLO(model_path)
    print(f"✅ YOLO26 model loaded successfully")
    return model


def benchmark_inference(model, device, num_iterations=100, imgsz=640):
    """Benchmark YOLO inference"""
    print(f"\n🚀 Running Benchmark")
    print(f"   Iterations: {num_iterations}")
    print(f"   Image Size: {imgsz}x{imgsz}")
    print(f"   Device: {device}")
    
    # Create dummy frame
    dummy_frame = np.random.randint(0, 255, (imgsz, imgsz, 3), dtype=np.uint8)
    
    # Warmup
    print("\n🔥 Warming up...")
    for _ in range(10):
        _ = model(dummy_frame, device=device, verbose=False)
    
    # Benchmark
    print("⏱️  Running benchmark...")
    times = []
    
    for i in range(num_iterations):
        start = time.perf_counter()
        _ = model(dummy_frame, device=device, verbose=False)
        elapsed = time.perf_counter() - start
        times.append(elapsed * 1000)  # Convert to ms
    
    # Statistics
    avg_time = np.mean(times)
    std_time = np.std(times)
    min_time = np.min(times)
    max_time = np.max(times)
    fps = 1000 / avg_time
    
    print(f"\n📊 Results")
    print(f"   Average: {avg_time:.2f} ms")
    print(f"   Std Dev: {std_time:.2f} ms")
    print(f"   Min: {min_time:.2f} ms")
    print(f"   Max: {max_time:.2f} ms")
    print(f"   FPS: {fps:.1f}")
    
    return {
        'avg_ms': avg_time,
        'std_ms': std_time,
        'min_ms': min_time,
        'max_ms': max_time,
        'fps': fps
    }


def compare_devices(model):
    """Compare performance across devices"""
    print("\n" + "=" * 50)
    print("📈 Device Comparison")
    print("=" * 50)
    
    devices = []
    if torch.backends.mps.is_available():
        devices.append('mps')
    if torch.cuda.is_available():
        devices.append('cuda')
    devices.append('cpu')
    
    results = {}
    
    for device in devices:
        print(f"\n🔴 Testing {device.upper()}...")
        results[device] = benchmark_inference(model, device, num_iterations=50)
    
    print("\n" + "=" * 50)
    print("📊 Comparison Summary")
    print("=" * 50)
    
    for device, stats in results.items():
        print(f"{device.upper():8s}: {stats['fps']:6.1f} FPS ({stats['avg_ms']:.2f} ms)")
    
    if 'mps' in results and 'cpu' in results:
        speedup = results['mps']['fps'] / results['cpu']['fps']
        print(f"\n🚀 MPS Speedup: {speedup:.2f}x faster than CPU")
    
    return results


def main():
    """Main benchmark function"""
    print("\n" + "=" * 50)
    print("🎮 YOLO26 Fruit Ninja - MPS Benchmark")
    print("=" * 50)
    
    # Check device
    device = check_device()
    
    # Load YOLO26 model
    model = load_model("yolo26n.pt")

    # Move model to device
    model.to(device)
    
    # Run benchmark
    results = benchmark_inference(model, device, num_iterations=100)
    
    # Compare devices (optional, takes longer)
    # compare_devices(model)
    
    print("\n" + "=" * 50)
    print("✅ Benchmark Complete")
    print("=" * 50)
    
    # Performance rating
    fps = results['fps']
    if fps >= 60:
        rating = "🟢 Excellent - Ready for real-time gameplay"
    elif fps >= 30:
        rating = "🟡 Good - Playable with minor lag"
    else:
        rating = "🔴 Poor - Consider reducing model size"
    
    print(f"\n📈 Performance Rating: {rating}")
    
    return results


if __name__ == "__main__":
    main()
