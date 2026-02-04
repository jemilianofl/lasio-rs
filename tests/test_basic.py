import lasio_rs
import time
import os

print("=" * 60)
print("LAS_read_rs Comprehensive Test with 09.las")
print("=" * 60)

filename = "sample.las"
if not os.path.exists(filename):
    print(f"Error: {filename} not found")
    exit(1)

print(f"\nFile: {filename} ({os.path.getsize(filename) / 1024 / 1024:.2f} MB)")

# 1. Read timing
print("\n1. Reading LAS file...")
start = time.time()
las = lasio_rs.read(filename)
read_time = time.time() - start
print(f"   Read time: {read_time:.4f} seconds")

# 2. Display metadata
print("\n2. Metadata:")
print(
    f"   Version: {las.version['VERS'].value if 'VERS' in las.version.keys() else 'N/A'}"
)
print(f"   Well: {las.well['WELL'].value if 'WELL' in las.well.keys() else 'N/A'}")
print(f"   Number of curves: {len(list(las.curves.keys()))}")

# 3. Show first 5 curves
print("\n3. First 5 Curves:")
for i, mnem in enumerate(list(las.curves.keys())[:5]):
    curve = las.curves[mnem]
    print(f"   {mnem} ({curve.unit}): {len(curve.data)} points")

# 4. Convert to DataFrame
print("\n4. Converting to pandas DataFrame...")
try:
    df = las.to_df()
    print(f"   DataFrame shape: {df.shape}")
    print(f"   Columns: {list(df.columns)[:5]}... ({len(df.columns)} total)")
    print("\n   First 5 rows:")
    print(df.head())
except Exception as e:
    print(f"   Error: {e}")

# 5. Export to CSV
print("\n5. Exporting to CSV...")
try:
    las.to_csv("output_sample.csv")
    print(f"   Saved: output_sample.csv ({os.path.getsize('output_sample.csv') / 1024:.1f} KB)")
except Exception as e:
    print(f"   Error: {e}")

# 6. Export to LAS 2.0
print("\n6. Exporting to LAS 2.0...")
try:
    las.to_las("output_sample_v2.las", version="2.0")
    print(
        f"   Saved: output_sample_v2.las ({os.path.getsize('output_sample_v2.las') / 1024:.1f} KB)"
    )
except Exception as e:
    print(f"   Error: {e}")

# 7. Export to LAS 3.0
print("\n7. Exporting to LAS 3.0...")
try:
    las.to_las("output_sample_v3.las", version="3.0")
    print(
        f"   Saved: output_sample_v3.las ({os.path.getsize('output_sample_v3.las') / 1024:.1f} KB)"
    )
except Exception as e:
    print(f"   Error: {e}")

# 8. Export to Excel
print("\n8. Exporting to Excel...")
try:
    las.to_excel("output_sample.xlsx")
    print(
        f"   Saved: output_sample.xlsx ({os.path.getsize('output_sample.xlsx') / 1024:.1f} KB)"
    )
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
