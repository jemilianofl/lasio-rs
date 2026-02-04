import timeit
import sys
import os

# sys.path.insert(0, os.path.join(os.getcwd(), "lasio")) # Comparison against installed lasio

SETUP = """
import lasio_rs
import lasio
import os

filename = "09.las"
"""

TEST_RUST = """
las = lasio_rs.read(filename)
"""

TEST_PYTHON = """
las = lasio.read(filename)
"""

if __name__ == "__main__":
    if not os.path.exists("09.las"):
        print("Error: 09.las not found.")
        sys.exit(1)

    print(
        f"Benchmarking with file: 09.las ({os.path.getsize('09.las') / 1024 / 1024:.2f} MB)"
    )

    # Rust Benchmark
    print("Running Rust lasio-rs...")
    rust_times = timeit.repeat(TEST_RUST, setup=SETUP, repeat=5, number=1)
    avg_rust = sum(rust_times) / len(rust_times)
    print(f"Rust average time: {avg_rust:.4f} s")

    # Python Benchmark
    print("Running Python lasio...")
    try:
        py_times = timeit.repeat(TEST_PYTHON, setup=SETUP, repeat=5, number=1)
        avg_py = sum(py_times) / len(py_times)
        print(f"Python average time: {avg_py:.4f} s")

        speedup = avg_py / avg_rust
        print(f"\n🚀 Speedup: {speedup:.2f}x faster")
    except Exception as e:
        print(f"Python benchmark failed: {e}")
