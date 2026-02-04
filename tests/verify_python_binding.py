import lasio_rs
import os

# Create a sample file if not exists
if not os.path.exists("sample.las"):
    with open("sample.las", "w") as f:
        f.write(
            "~Version\nVERS. 2.0 : CWLS\nWRAP. NO : One line\n~Well\nSTRT.M 1670.0 : Start\nSTOP.M 1669.75 : Stop\nSTEP.M -0.125 : Step\nNULL. -999.25 : Null\n~Curves\nDEPT.M : Depth\nDT.US/M : Sonic\n~ASCII\n1670.0 123.45\n1669.875 -999.25\n1669.75 124.50\n"
        )

print("Attempting to read sample.las with lasio_rs...")
try:
    las = lasio_rs.read("sample.las")
    print("Successfully read LAS file!")
    print(f"Version: {las.version}")

    # We exposed 'well_name' as a test getter in pybindings.rs getting 'WELL' item
    # But sample.las doesn't have WELL item in ~Well, it has STRT, STOP etc.
    # Let's just check if we got an object.
    print(f"LAS Object: {las}")
    print("Verification Successful!")
except Exception as e:
    print(f"Verification Failed: {e}")
    exit(1)
