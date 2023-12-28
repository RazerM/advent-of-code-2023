// Note: I'm only using rust for day 2 because I wanted to refamiliarise myself with nom.
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::str::FromStr;

use nom::branch::alt;
use nom::bytes::complete::tag;
use nom::character::complete::{char, digit1, multispace0, space0, space1};
use nom::combinator::{map_res, recognize};
use nom::error::ParseError;
use nom::multi::separated_list0;
use nom::sequence::{delimited, separated_pair, terminated, tuple};
use nom::IResult;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use thiserror::Error;

#[derive(Debug, PartialEq, Eq)]
#[pyclass]
struct Game {
    #[pyo3(get)]
    id: u32,
    #[pyo3(get)]
    sets: Vec<Vec<(u32, Colour)>>,
}

#[pymethods]
impl Game {
    fn __repr__(&self) -> String {
        format!("<Game id={}>", self.id)
    }
}

#[pyclass]
#[pyo3(rename_all = "SCREAMING_SNAKE_CASE")]
#[derive(PartialEq, Eq, Clone, Debug, Hash)]
enum Colour {
    Red,
    Green,
    Blue,
}

#[pymethods]
impl Colour {
    fn __hash__(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.hash(&mut hasher);
        hasher.finish()
    }
}

#[derive(Error, Debug)]
#[error("invalid colour")]
struct ParseColourError;

impl FromStr for Colour {
    type Err = ParseColourError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "red" => Ok(Colour::Red),
            "green" => Ok(Colour::Green),
            "blue" => Ok(Colour::Blue),
            _ => Err(ParseColourError),
        }
    }
}

fn ws<'a, F: 'a, O, E: ParseError<&'a str>>(
    inner: F,
) -> impl FnMut(&'a str) -> IResult<&'a str, O, E>
where
    F: Fn(&'a str) -> IResult<&'a str, O, E>,
{
    delimited(space0, inner, space0)
}

fn integer(input: &str) -> IResult<&str, u32> {
    map_res(recognize(digit1), str::parse)(input)
}

fn colour(input: &str) -> IResult<&str, Colour> {
    map_res(
        recognize(alt((tag("red"), tag("green"), tag("blue")))),
        str::parse,
    )(input)
}

/// Parse `Game <id>:` part
fn prefix(input: &str) -> IResult<&str, u32> {
    let mut parser = tuple((space0, tag("Game"), space1, integer, char(':')));
    let (input, (_, _, _, game_id, _)) = parser(input)?;
    Ok((input, game_id))
}

fn game(input: &str) -> IResult<&str, Game> {
    let (input, game_id) = terminated(prefix, space0)(input)?;

    let set = separated_list0(ws(char(',')), separated_pair(integer, space1, colour));
    let (input, sets) = separated_list0(ws(char(';')), set)(input)?;
    Ok((input, Game { id: game_id, sets }))
}

#[pyfunction]
fn parse_game(input: &str) -> PyResult<Game> {
    match terminated(game, multispace0)(input) {
        Ok(("", game)) => Ok(game),
        Ok(_) | Err(_) => Err(PyValueError::new_err("invalid game")),
    }
}

pub fn create_submodule<'a>(py: Python<'a>, m: &'a PyModule) -> PyResult<&'a PyModule> {
    let submodname = format!("{}.day02", m.name()?);
    let submod = PyModule::new(py, &submodname)?;
    submod.add_function(wrap_pyfunction!(parse_game, submod)?)?;
    submod.add_class::<Colour>()?;
    submod.add_class::<Game>()?;

    py.import("sys")?
        .getattr("modules")?
        .set_item(&submodname, submod)?;

    Ok(submod)
}

#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn parse_prefix() {
        assert_eq!(prefix("Game 42:"), Ok(("", 42)));
    }
    #[test]
    fn parse_game() {
        assert_eq!(
            game("Game 1: 1 red, 2 blue; 3 blue, 4 green\n"),
            Ok((
                "",
                Game {
                    id: 1,
                    sets: vec![
                        vec![(1, Colour::Red), (2, Colour::Blue)],
                        vec![(3, Colour::Blue), (4, Colour::Green)]
                    ]
                }
            ))
        );
    }
}
