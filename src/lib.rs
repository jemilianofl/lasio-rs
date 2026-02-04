pub mod las_items;
pub mod reader;
// Conditional compilation for python bindings? 
// Or just always expose if feature enabled? 
// For now, let's include it.
// We just need pybindings.
pub mod pybindings;

use indexmap::IndexMap;
pub use las_items::{CurveItem, HeaderItem}; 
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct LASFile {
    pub version: SectionItems,
    pub well: SectionItems,
    pub curves: SectionCurves, 
    pub params: SectionItems,
    pub other: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct SectionItems {
    #[serde(flatten)]
    pub items: IndexMap<String, HeaderItem>, 
}

impl SectionItems {
    pub fn new() -> Self {
        Self {
            items: IndexMap::new(),
        }
    }

    pub fn insert(&mut self, item: HeaderItem) {
        self.items.insert(item.mnemonic.clone(), item);
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct SectionCurves {
     #[serde(flatten)]
    pub items: IndexMap<String, CurveItem>,
}

impl SectionCurves {
     pub fn new() -> Self {
        Self {
            items: IndexMap::new(),
        }
    }
    
    pub fn insert(&mut self, item: CurveItem) {
        self.items.insert(item.mnemonic.clone(), item);
    }
}


impl LASFile {
    pub fn new() -> Self {
        Self::default()
    }
}

// We need to re-export the pymodule entry point if we want it to be found by python
// No cfg needed here since pybindings is already pub mod above.
// pub mod pybindings; // We only declare mod once. 
