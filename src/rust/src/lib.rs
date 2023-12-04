#![deny(rust_2018_idioms)]

use pyo3::prelude::*;

mod day02;

#[pymodule]
fn _rust(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_submodule(day02::create_submodule(py, m)?)?;

    Ok(())
}
