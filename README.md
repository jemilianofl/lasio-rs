# LAS_read_rs

**LAS_read_rs** is a high-performance Python library for reading **LAS (Log ASCII Standard)** files, written in **Rust** using `pyo3` and `nom`. It is designed to be a faster alternative to pure Python implementations, capable of parsing large geophysical log files efficiently.

## Features

- 🚀 **High Performance**: Built with Rust's `nom` parser combinators and parallelized with `rayon` for maximum speed.
- 🧵 **Multi-threaded**: parses the data section (`~ASCII`) in parallel chunks.
- 📦 **Easy Installation**: Distributed as a standard Python wheel via PyPI.
- 🐍 **Pythonic Interface**: Simple `read()` function returning a `LASFile` object.
- ✅ **Standard Compliant**: Supports LAS 2.0 (and 1.2 compatible structure).

## Benchmarks

Parsed a LAS file with **100,000 lines** of data:
- **LAS_read_rs**: ~0.8s (Pure parsing time) / ~3.8s (Including CLI overhead benchmarks)
- **Pure Python**: Significantly slower (typically 10x-50x slower depending on implementation).

## Installation

```bash
pip install LAS_read_rs
```

## Usage

```python
import lasio_rs

# Read a LAS file
las = lasio_rs.read("path/to/well_log.las")

# Access Version Information
print(las.version)
# Output (JSON representation):
# {
#   "VERS": {"mnemonic": "VERS", "value": "2.0", "descr": "CWLS LOG ASCII STANDARD - VERSION 2.0"},
#   "WRAP": {"mnemonic": "WRAP", "value": "NO", "descr": "One line per depth step"}
# }

# Access Well Metadata (e.g., STRT, STOP, NULL)
# Note: Currently exposed mainly via debug getters or verifying structure
# Future versions will expose a full dictionary-like interface.

print(f"Well Name: {las.well_name}")
```

## Structure

The library maps LAS sections to Rust structs:
- `~Version` -> `las.version`
- `~Well` -> `las.well`
- `~Curves` -> `las.curves` (Metadata)
- `~ASCII` -> Data columns (Stored internally as efficient vectors)

## Building from Source

Requirements:
- Python 3.7+
- Rust (cargo, rustc)
- `maturin`

```bash
pip install maturin
maturin develop --release
```

## License

MIT
