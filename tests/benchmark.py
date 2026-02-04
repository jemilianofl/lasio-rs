import timeit
import os
import sys
import numpy

# Ensure local lasio is importable
sys.path.insert(0, os.path.join(os.getcwd(), "lasio"))

SETUP_CODE = """
import subprocess
import json
import os

filepath = "sample.las"

def run_rust():
    # Start the process
    # Note: --quiet reduces overhead slightly but cargo run still checks build
    subprocess.run(["cargo", "run", "--quiet", "--bin", "lasio_json", "--", filepath], capture_output=True)

"""

PYTHON_TEST = """
import lasio
lasio.read(filepath)
"""

RUST_TEST = """
run_rust()
"""

if __name__ == "__main__":
    # Create a larger sample file for meaningful benchmark
    with open("big_sample.las", "w") as f:
        f.write(
            "~Version\nVERS. 2.0 : CWLS\nWRAP. NO : One line\n~Well\nSTRT.M 0.0 : Start\nSTOP.M 1000.0 : Stop\nSTEP.M 1.0 : Step\nNULL. -999.25 : Null\n~Curves\nDEPT.M : Depth\nDT.US/M : Sonic\n~ASCII\n"
        )
        for i in range(100000):
            f.write(f"{i * 1.0} {100.0 + (i % 50)}\n")

    SETUP_CODE_BIG = SETUP_CODE.replace(
        'filepath = "sample.las"', 'filepath = "big_sample.las"'
    )

    try:
        import lasio

        # Check if numpy is available, as lasio needs it
        import numpy

        print("Benchmarking Python lasio...")
        py_time = timeit.timeit(PYTHON_TEST, setup=SETUP_CODE_BIG, number=5)
        print(f"Python: {py_time:.4f}s for 5 runs")
    except ImportError:
        print("Skipping Python benchmark (lasio or numpy not installed).")

    print("Benchmarking Rust lasio-rs (CLI mode)...")
    rust_time = timeit.timeit(RUST_TEST, setup=SETUP_CODE_BIG, number=5)
    print(f"Rust (CLI): {rust_time:.4f}s for 5 runs")

    # Cleanup
    if os.path.exists("big_sample.las"):
        os.remove("big_sample.las")
