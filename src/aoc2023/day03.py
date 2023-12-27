import math
from collections import defaultdict
from typing import IO

from ._registry import register
from ._util import Grid, Vector


def is_symbol(char: str) -> bool:
    assert len(char) == 1
    return char != "." and not char.isdigit()


@register(day=3)
def solve(file: IO[str], verbose: int) -> None:
    grid = Grid([[c for c in line.rstrip()] for line in file])
    part_numbers = []
    width = grid.width
    gear_numbers: defaultdict[Vector[int], list[int]] = defaultdict(list)
    for y, row in enumerate(grid):
        number_chars = []
        is_part = False
        cogs: set[Vector[int]] = set()
        for x, char in enumerate(row):
            pos = Vector(x, y)
            isdigit = char.isdigit()
            if isdigit:
                number_chars.append(char)
                for loc in grid.neighbours(pos):
                    if not is_part and is_symbol(grid[loc]):
                        is_part = True
                    if grid[loc] == "*":
                        cogs.add(loc)

            if not isdigit or x == width - 1:
                if number_chars:
                    if is_part:
                        number = int("".join(number_chars))
                        part_numbers.append(number)
                        for loc in cogs:
                            gear_numbers[loc].append(number)
                    number_chars = []
                    is_part = False
                    cogs = set()

    gear_ratios = []

    for numbers in gear_numbers.values():
        if len(numbers) == 2:
            gear_ratios.append(math.prod(numbers))

    print("Part 1:", sum(part_numbers))
    print("Part 2:", sum(gear_ratios))
