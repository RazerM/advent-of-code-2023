# Installation

```bash
git clone https://github.com/RazerM/advent-of-code-2023
cd advent-of-code-2023
python3 -m venv --prompt aoc2023 .venv
source .venv/bin/activate
pip install -e .
```

# CLI

Set the `AOC_SESSION` environment variable to the value of your
https://adventofcode.com `session` cookie. It may also be added to an `.env`
file.

## Manual Commands

```bash
aoc2023 download 1 input/1.txt
```

```bash
aoc2023 run 1 input/1.txt
```

## Automatic Commands

These commands assume an `input` directory is being used. Use `prepare` to
download all available input files and create any missing python modules in
`src/aoc2023` from a template.

```bash
aoc2023 prepare
```

Run the solution for the current day (or provide it as an argument). Uses
the corresponding input file automatically.

```bash
aoc2023 autorun [day]
```
