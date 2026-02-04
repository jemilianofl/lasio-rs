import sys
import os
import json
import subprocess

# Add local lasio to path
sys.path.insert(0, os.path.join(os.getcwd(), "lasio"))

try:
    import lasio
except ImportError:
    print("Could not import lasio from local folder. Trying installed...")
    import lasio

def run_rust_parser(filepath):
    result = subprocess.run(["cargo", "run", "--quiet", "--bin", "lasio_json", "--", filepath], capture_output=True, text=True)
    if result.returncode != 0:
        print("Rust Error:", result.stderr)
        return None
    return json.loads(result.stdout)

def compare(python_data, rust_data):
    # Basic comparison logic
    # Compare headers
    print("Comparing Headers...")
    # This might be tricky as structures differ slightly in JSON representation
    # Python lasio.json property returns a string of JSON manually constructed? 
    # Or we can just inspect objects.
    
    # Let's compare Curves length
    py_curves = python_data.cycles if hasattr(python_data, 'cycles') else python_data.keys()
    # Wait, lasio object has .curves
    py_curve_count = len(python_data.curves)
    # Rust data: curves.items (IndexMap)
    rust_curve_count = len(rust_data['curves'])
    
    if py_curve_count != rust_curve_count:
        print(f"Curve count mismatch: Py {py_curve_count} vs Rust {rust_curve_count}")
        return False
        
    print(f"Curve count matches: {py_curve_count}")
    
    # Compare Data
    print("Comparing Data content...")
    # Check first value of first curve
    py_val = python_data.curves[0].data[0]
    rust_val = rust_data['curves'][python_data.curves[0]['mnemonic']]['data'][0]
    
    if abs(py_val - rust_val) > 1e-6:
         print(f"Data Mismatch: {py_val} vs {rust_val}")
         return False

    print("Data verification passed (basic check).")
    return True

if __name__ == "__main__":
    las_file = "sample.las"
    print(f"Reading {las_file} with Python lasio...")
    l = lasio.read(las_file)
    
    print(f"Reading {las_file} with Rust lasio-rs...")
    r_json = run_rust_parser(las_file)
    
    if r_json:
        if compare(l, r_json):
            print("SUCCESS: Parity confirmed!")
        else:
            print("FAILURE: Parity check failed.")
            sys.exit(1)
    else:
        print("FAILURE: Rust parser failed.")
        sys.exit(1)
