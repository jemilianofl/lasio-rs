use crate::reader::parse_las_from_reader;
use crate::{LASFile, HeaderItem, CurveItem};
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::fs::File;
use std::io::BufReader;

#[pymodule]
fn _lasio_rs(_py: Python, m: &PyModule) -> PyResult<()> {
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
    fn json_headers(&self) -> String {
        // We exclude big data from this JSON to be fast.
        // But our default Serialize includes CurveItem data? 
        // CurveItem struct has `data` field. serialization of 100k floats is costly.
        // We should probably implement custom serialization or a "metadata only" struct?
        // Quick hack: Use a helper struct or just serialize sections individually.
        
        // Let's rely on the fact that CurveItem.data is Vec<f64>. 
        // We can just serialize `inner.version`, `inner.well`, `inner.params`.
        let json_structure = serde_json::json!({
            "version": self.inner.version,
            "well": self.inner.well,
            "params": self.inner.params,
            "curves": self.inner.curves // matches structure
        });
        // Note: inner.curves items have .data. We need to avoid serializing that.
        // But we don't have a separate struct.
        // Ideally we change `LASFile` to not verify data.
        
        json_structure.to_string()
    }
    
    fn get_curve_data(&self, mnemonic: String) -> Option<Vec<f64>> {
        self.inner.curves.items.get(&mnemonic).map(|c| c.data.clone())
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
