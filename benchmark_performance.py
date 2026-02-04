"""
Performance Benchmark: lasio_rs (Rust) vs lasio (Python)
"""

import time
import os
import sys

# File to benchmark
FILENAME = "09.las"

if not os.path.exists(FILENAME):
    print(f"Error: {FILENAME} not found")
    sys.exit(1)

file_size_mb = os.path.getsize(FILENAME) / 1024 / 1024
print("=" * 70)
print(f"PERFORMANCE BENCHMARK: lasio_rs vs lasio")
print(f"File: {FILENAME} ({file_size_mb:.2f} MB)")
print("=" * 70)

# Number of iterations
ITERATIONS = 3

# Benchmark lasio_rs (Rust)
print(f"\n🦀 Testing lasio_rs (Rust)...")
try:
    import lasio_rs

    rust_times = []
    for i in range(ITERATIONS):
        start = time.perf_counter()
        las = lasio_rs.read(FILENAME)
        elapsed = time.perf_counter() - start
        rust_times.append(elapsed)
        print(f"   Run {i + 1}: {elapsed:.4f}s")

    rust_avg = sum(rust_times) / len(rust_times)
    rust_min = min(rust_times)
    print(f"   Average: {rust_avg:.4f}s | Best: {rust_min:.4f}s")
    print(
        f"   Curves: {len(list(las.curves.keys()))} | Points per curve: {len(las.curves[list(las.curves.keys())[0]].data)}"
    )
except Exception as e:
    print(f"   Error: {e}")
    rust_avg = None

# Benchmark lasio (Python)
print(f"\n🐍 Testing lasio (Python)...")
try:
    import lasio

    python_times = []
    for i in range(ITERATIONS):
        start = time.perf_counter()
        las = lasio.read(FILENAME)
        elapsed = time.perf_counter() - start
        python_times.append(elapsed)
        print(f"   Run {i + 1}: {elapsed:.4f}s")

    python_avg = sum(python_times) / len(python_times)
    python_min = min(python_times)
    print(f"   Average: {python_avg:.4f}s | Best: {python_min:.4f}s")
    print(f"   Curves: {len(las.curves)} | Points per curve: {len(las.curves[0].data)}")
except Exception as e:
    print(f"   Error: {e}")
    python_avg = None

# Results
print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

if rust_avg and python_avg:
    speedup = python_avg / rust_avg
    print(f"\n   lasio_rs (Rust):  {rust_avg:.4f}s average")
    print(f"   lasio (Python):   {python_avg:.4f}s average")
    print(f"\n   🚀 SPEEDUP: {speedup:.2f}x faster with Rust!")

    if speedup > 1:
        print(f"\n   ✅ lasio_rs is {speedup:.1f}x FASTER than lasio")
    else:
        print(f"\n   ⚠️ lasio is {1 / speedup:.1f}x faster than lasio_rs")
elif rust_avg:
    print(f"\n   lasio_rs (Rust):  {rust_avg:.4f}s average")
    print(f"   lasio (Python):   FAILED")
elif python_avg:
    print(f"\n   lasio_rs (Rust):  FAILED")
    print(f"   lasio (Python):   {python_avg:.4f}s average")

print("\n" + "=" * 70)
