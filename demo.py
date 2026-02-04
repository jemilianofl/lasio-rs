import lasio_rs
import json
import os

# 1. Create a dummy LAS file
las_content = """~Version Information
VERS.                  2.0 :   CWLS LOG ASCII STANDARD - VERSION 2.0
WRAP.                  NO  :   One line per depth step
~Well Information
STRT.M                 100.0 : Start Depth
STOP.M                 101.0 : Stop Depth
STEP.M                 0.5   : Step
NULL.                  -999.25   : Null Value
COMP.                  iGeoz Demo : Company
WELL.                  DEMO-001   : Well
~Curve Information
DEPT.M                      :  1  DEPTH
GR.GAPI                     :  2  GAMMA RAY
RHOB.G/C3                   :  3  BULK DENSITY
~ASCII
100.0   45.2   2.35
100.5   48.1   2.38
101.0   42.0   2.34
"""

filename = "demo_well.las"
with open(filename, "w") as f:
    f.write(las_content)

print(f"--- Created {filename} ---")

# 2. Read using Rust library
print("\n--- Reading with LAS_read_rs (Rust) ---")
try:
    las = lasio_rs.read(filename)
    print("✅ File Parsed Successfully!")
except Exception as e:
    print(f"❌ Parsing Failed: {e}")
    exit(1)

# 3. Display Metadata
print("\n--- Header Info ---")
print(f"Version: {las.version['VERS'].value}")
print(f"Wrap:    {las.version['WRAP'].value}")
print(f"Well:    {las.well['WELL'].value}")
print(f"Start:   {las.well['STRT'].value}")
print(f"Stop:    {las.well['STOP'].value}")

# 4. Display Curve Data
print("\n--- Curve Data ---")
for mnemonic in las.keys():
    curve = las.curves[mnemonic]
    print(f"{mnemonic} ({curve.unit}): {curve.data} -- {curve.descr}")

# 5. Access specific data
gr_vals = las["GR"]
print(f"\nGamma Ray values directly: {gr_vals}")

print("\n✅ DEMO COMPLETE: The library is installed and working correctly.")
