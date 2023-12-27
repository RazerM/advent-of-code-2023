from collections import deque
from functools import cache
from typing import IO

from ._registry import register


def rotate(lines: list[str]) -> list[str]:
    """Rotate a list of lines by 90 degrees anti-clockwise

    ABCDE
    12345

    becomes

    E5
    D4
    C3
    B2
    A1
    """
    return ["".join(col) for col in reversed(list(zip(*lines)))]


def tilt(column: str) -> str:
    return "#".join("".join(sorted(x, reverse=True)) for x in column.split("#"))


def calculate_load(columns: list[str]) -> int:
    load = 0
    for column in columns:
        height = len(column)
        for y, c in enumerate(column):
            if c == "O":
                load += height - y
    return load


def format_columns(columns: list[str]) -> str:
    return "\n".join(reversed(rotate(columns)))


def print_columns(columns: list[str]) -> None:
    print(format_columns(columns))


@register(day=14)
def solve(file: IO[str], verbose: int) -> None:
    lines = [line.rstrip() for line in file]
    initial_columns = list("".join(col) for col in zip(*lines))

    columns = initial_columns.copy()
    for i, column in enumerate(columns):
        columns[i] = tilt(column)

    print("Part 1:", calculate_load(columns))

    columns = initial_columns.copy()
    column_cycles = dict()
    cycle = 0
    cycles = 1000000000
    found = False
    while cycle < cycles:
        for _ in range(4):
            for i, column in enumerate(columns):
                columns[i] = tilt(column)
            columns = rotate(columns)

        if verbose >= 3:
            print(f"After {cycle + 1} cycle{'s' if cycle > 1 else ''}:")
            print_columns(columns)
            print(f"load={calculate_load(columns)}")
            print()

        if not found:
            key = format_columns(columns)
            if key in column_cycles:
                found = True
                first_cycle = column_cycles[key]
                remaining_cycles = cycles - cycle
                cycle_length = cycle - first_cycle
                cycle = cycles - (remaining_cycles % cycle_length)
            else:
                column_cycles[key] = cycle
        cycle += 1

    print("Part 2:", calculate_load(columns))
