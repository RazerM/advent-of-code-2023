use std::collections::VecDeque;
use std::num::TryFromIntError;
use std::ops::Add;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use rustc_hash::{FxHashMap, FxHashSet};
use thiserror::Error;

#[derive(Copy, Clone, Debug, Hash, Eq, PartialEq, FromPyObject)]
struct Vector {
    x: i32,
    y: i32,
}

impl Add for Vector {
    type Output = Self;

    fn add(self, other: Self) -> Self::Output {
        Vector {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Vector {
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }
}

#[derive(Clone, Debug, FromPyObject)]
struct Grid {
    #[pyo3(attribute("_grid"))]
    grid: Vec<Vec<char>>,
    width: usize,
    height: usize,
}

#[derive(Error, Debug)]
#[error("out of bounds")]
struct BoundsError;

impl From<TryFromIntError> for BoundsError {
    fn from(_: TryFromIntError) -> Self {
        BoundsError
    }
}

impl From<BoundsError> for PyErr {
    fn from(_: BoundsError) -> Self {
        PyValueError::new_err("out of bounds")
    }
}

impl Grid {
    fn get(&self, loc: &Vector) -> Result<&char, BoundsError> {
        let y: usize = loc.y.try_into()?;
        let x: usize = loc.x.try_into()?;
        self.grid
            .get(y)
            .and_then(|row| row.get(x))
            .ok_or(BoundsError)
    }
}

#[pyclass]
#[pyo3(rename_all = "SCREAMING_SNAKE_CASE")]
#[derive(Copy, Clone, Debug, Hash, Eq, PartialEq)]
enum Direction {
    Right,
    Down,
    Left,
    Up,
}

impl Direction {
    fn vertical(&self) -> bool {
        matches!(self, Self::Up | Self::Down)
    }

    fn horizontal(&self) -> bool {
        matches!(self, Self::Left | Self::Right)
    }

    fn to_vec(self) -> Vector {
        match self {
            Direction::Right => Vector::new(1, 0),
            Direction::Down => Vector::new(0, 1),
            Direction::Left => Vector::new(-1, 0),
            Direction::Up => Vector::new(0, -1),
        }
    }
}

#[pyfunction]
#[pyo3(name = "fire_laser")]
fn fire_laser_py(grid: Grid, pos: Vector, direction: Direction) -> usize {
    fire_laser(&grid, pos, direction)
}

fn fire_laser(grid: &Grid, pos: Vector, direction: Direction) -> usize {
    let mut queue = VecDeque::from([(pos, direction)]);
    let mut visited = FxHashMap::<Vector, FxHashSet<Direction>>::default();
    while let Some((pos, direction)) = queue.pop_front() {
        let tile = match grid.get(&pos) {
            Ok(tile) => tile,
            Err(BoundsError) => continue,
        };
        if !visited.entry(pos).or_default().insert(direction) {
            continue;
        }
        match tile {
            '\\' => {
                let direction = match direction {
                    Direction::Right => Direction::Down,
                    Direction::Down => Direction::Right,
                    Direction::Left => Direction::Up,
                    Direction::Up => Direction::Left,
                };
                queue.push_back((pos + direction.to_vec(), direction));
            }
            '/' => {
                let direction = match direction {
                    Direction::Right => Direction::Up,
                    Direction::Down => Direction::Left,
                    Direction::Left => Direction::Down,
                    Direction::Up => Direction::Right,
                };
                queue.push_back((pos + direction.to_vec(), direction));
            }
            '|' if direction.horizontal() => {
                queue.push_back((pos + Direction::Up.to_vec(), Direction::Up));
                queue.push_back((pos + Direction::Down.to_vec(), Direction::Down));
            }
            '-' if direction.vertical() => {
                queue.push_back((pos + Direction::Left.to_vec(), Direction::Left));
                queue.push_back((pos + Direction::Right.to_vec(), Direction::Right));
            }
            _ => {
                queue.push_back((pos + direction.to_vec(), direction));
            }
        }
    }
    // A position is energized if we've visited it
    visited.len()
}

#[pyfunction]
fn max_edge_energized(grid: Grid) -> usize {
    let mut configurations = Vec::with_capacity(grid.width * grid.height);
    for x in 0..grid.width {
        configurations.push((Vector::new(x as i32, 0), Direction::Down));
        configurations.push((
            Vector::new(x as i32, (grid.height - 1) as i32),
            Direction::Up,
        ));
    }
    for y in 0..grid.height {
        configurations.push((Vector::new(0, y as i32), Direction::Right));
        configurations.push((
            Vector::new((grid.width - 1) as i32, y as i32),
            Direction::Left,
        ));
    }
    configurations
        .into_iter()
        .map(|(pos, direction)| fire_laser(&grid, pos, direction))
        .max()
        .expect("not empty")
}

pub fn create_submodule<'a>(py: Python<'a>, m: &'a PyModule) -> PyResult<&'a PyModule> {
    let submodname = format!("{}.day16", m.name()?);
    let submod = PyModule::new(py, &submodname)?;
    submod.add_function(wrap_pyfunction!(fire_laser_py, submod)?)?;
    submod.add_function(wrap_pyfunction!(max_edge_energized, submod)?)?;
    submod.add_class::<Direction>()?;

    py.import("sys")?
        .getattr("modules")?
        .set_item(&submodname, submod)?;

    Ok(submod)
}
