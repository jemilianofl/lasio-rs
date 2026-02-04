# las_read_rs 🦀

[![PyPI version](https://badge.fury.io/py/las-read-rs.svg)](https://pypi.org/project/las-read-rs/)
[![CI](https://github.com/jemilianofl/lasio-rs/actions/workflows/ci.yml/badge.svg)](https://github.com/jemilianofl/lasio-rs/actions)

**High-performance LAS (Log ASCII Standard) file reader written in Rust** with Python bindings. A faster alternative to pure Python implementations, capable of parsing large geophysical log files efficiently.

## ⚡ Performance

Benchmarked with a **92 MB** LAS file (400 curves, 21,842 points each):

| Library | Read Time | Speedup |
|---------|-----------|---------|
| **las_read_rs** (Rust) | ~1.0s | **9x faster** 🚀 |
| lasio (Python) | ~9.0s | baseline |

## 🚀 Installation

```bash
pip install las_read_rs
```

**Optional dependencies for export features:**
```bash
pip install pandas          # For DataFrame and CSV export
pip install openpyxl        # For Excel export
pip install polars          # For Polars DataFrame
```

## 📖 Quick Start

```python
import lasio_rs

# Read a LAS file
las = lasio_rs.read("well_log.las")

# Access metadata
print(las.version['VERS'].value)  # "2.0"
print(las.well['WELL'].value)     # Well name

# Access curve data directly
depth = las['DEPT']  # Returns list of floats
gr = las['GR']       # Gamma Ray values

# List all curves
for curve_name in las.keys():
    curve = las.curves[curve_name]
    print(f"{curve_name} ({curve.unit}): {len(curve.data)} points")
```

## 📊 DataFrame Conversion

```python
# Convert to pandas DataFrame
df = las.to_df()
print(df.head())

# Convert to polars DataFrame
df_polars = las.to_polars()
```

## 💾 Export Formats

### CSV Export
```python
las.to_csv("output.csv")
```

### Excel Export
```python
las.to_excel("output.xlsx", sheet_name="Well Data")
```

### LAS Export (2.0 and 3.0)
```python
# Export as LAS 2.0
las.to_las("output_v2.las", version="2.0")

# Export as LAS 3.0
las.to_las("output_v3.las", version="3.0")
```

## 🔧 API Reference

### `lasio_rs.read(path)`
Reads a LAS file and returns a `LASFile` object.

### `LASFile` Properties
| Property | Description |
|----------|-------------|
| `version` | Version section (VERS, WRAP) |
| `well` | Well information (STRT, STOP, STEP, NULL, WELL, etc.) |
| `curves` | Curve metadata and data |
| `params` | Parameter section |

### `LASFile` Methods
| Method | Description |
|--------|-------------|
| `las[mnemonic]` | Get curve data as list |
| `las.keys()` | List curve mnemonics |
| `las.to_df()` | Convert to pandas DataFrame |
| `las.to_polars()` | Convert to polars DataFrame |
| `las.to_csv(path)` | Export to CSV |
| `las.to_excel(path)` | Export to Excel |
| `las.to_las(path, version)` | Export to LAS format |

## 🏗️ Building from Source

Requirements:
- Python 3.7+
- Rust (cargo, rustc)
- maturin

```bash
git clone https://github.com/jemilianofl/lasio-rs.git
cd lasio-rs
pip install maturin
maturin develop --release
```

## 📋 Supported LAS Versions

- ✅ LAS 2.0
- ✅ LAS 3.0 (read support)
- ✅ Export to LAS 2.0/3.0

## 🤝 Compatibility with lasio

`las_read_rs` provides a similar API to the popular `lasio` library:

```python
# lasio style
import lasio
las = lasio.read("file.las")
depth = las['DEPT']

# las_read_rs style (same!)
import lasio_rs
las = lasio_rs.read("file.las")
depth = las['DEPT']
```

## 📄 License

MIT

## 🙏 Acknowledgments

- Built with [PyO3](https://pyo3.rs/) for Python bindings
- Uses [nom](https://github.com/Geal/nom) for parsing
- Inspired by [lasio](https://github.com/kinverarity1/lasio)
