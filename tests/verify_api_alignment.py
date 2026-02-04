import lasio_rs
import os

# Ensure sample exists
if not os.path.exists("sample.las"):
    with open("sample.las", "w") as f:
        f.write(
            "~Version\nVERS. 2.0 : CWLS\nWRAP. NO : One line\n~Well\nSTRT.M 1670.0 : Start\nSTOP.M 1669.75 : Stop\nSTEP.M -0.125 : Step\nNULL. -999.25 : Null\n~Curves\nDEPT.M : Depth\nDT.US/M : Sonic\n~ASCII\n1670.0 123.45\n1669.875 -999.25\n1669.75 124.50\n"
        )

print("Reading file...")
las = lasio_rs.read("sample.las")

print("1. Testing .version attribute...")
print(las.version)
if las.version["VERS"].value != "2.0":
    raise Exception("Version check failed")

print("2. Testing .well attribute...")
print(las.well)
# Note: sample.las has STRT, STOP in ~Well.
if float(las.well["STRT"].value) != 1670.0:
    raise Exception("Well header check failed")

print("3. Testing curve data access via dictionary las['DEPT']...")
dept = las["DEPT"]
print(f"DEPT data: {dept}")
if len(dept) != 3:
    raise Exception("Data length check failed")
if abs(dept[0] - 1670.0) > 0.001:
    raise Exception("Data value check failed")

print("4. Testing curve object access las.curves['DT']...")
dt_curve = las.curves["DT"]
print(dt_curve)
if dt_curve.unit != "US/M":
    raise Exception("Curve unit check failed")

print("SUCCESS: API Alignment Verified!")
