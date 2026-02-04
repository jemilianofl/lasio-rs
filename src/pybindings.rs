use crate::reader::parse_las_from_reader;
use crate::{LASFile, HeaderItem, CurveItem};
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::fs::File;
use std::io::BufReader;

#[pymodule]
fn lasio_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyLASFile>()?;
    m.add_function(wrap_pyfunction!(read, m)?)?;
    Ok(())
}

#[pyclass(name = "LASFile")]
struct PyLASFile {
    inner: LASFile,
}

#[pymethods]
impl PyLASFile {
    #[getter]
    fn version(&self) -> String {
        // Return JSON representation for now or simple string
        format!("{:?}", self.inner.version)
    }
    
    // Simplification: just exposing basic metadata for speed test
    #[getter]
    fn well_name(&self) -> Option<String> {
         self.inner.well.items.get("WELL").map(|i| i.value.clone())
    }
}

#[pyfunction]
fn read(path: String) -> PyResult<PyLASFile> {
    let file = File::open(path).map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;
    let reader = BufReader::new(file);
    match parse_las_from_reader(reader) {
        Ok(las) => Ok(PyLASFile { inner: las }),
        Err(e) => Err(pyo3::exceptions::PyValueError::new_err(e.to_string())),
    }
}
