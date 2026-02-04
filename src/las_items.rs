use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HeaderItem {
    pub mnemonic: String,
    pub unit: String,
    pub value: String,
    pub descr: String,
}

impl HeaderItem {
    pub fn new(mnemonic: &str, unit: &str, value: &str, descr: &str) -> Self {
        Self {
            mnemonic: mnemonic.to_string(),
            unit: unit.to_string(),
            value: value.to_string(),
            descr: descr.to_string(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct CurveItem {
    pub mnemonic: String,
    pub unit: String,
    pub value: String, // API code or similar metadata
    pub descr: String,
    #[serde(skip)] // Don't serialize massive data array by default? Or maybe we want to. Python's json does.
    // For now, let's keep it simple. Arrays might be large.
    pub data: Vec<f64>, 
}

impl CurveItem {
    pub fn new(mnemonic: &str, unit: &str, value: &str, descr: &str) -> Self {
        Self {
            mnemonic: mnemonic.to_string(),
            unit: unit.to_string(),
            value: value.to_string(),
            descr: descr.to_string(),
            data: Vec::new(),
        }
    }
}
