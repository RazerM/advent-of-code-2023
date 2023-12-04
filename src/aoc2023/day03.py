import math
from collections import defaultdict
from collections.abc import Iterable, Iterator
from typing import IO

from ._registry import register


def is_symbol(char: str) -> bool:
    assert len(char) == 1
    return char != "." and not char.isdigit()


type GridLocation = tuple[int, int]


class Grid[T]:
    def __init__(self, grid: list[list[T]]) -> None:
        self._grid = grid

    @property
    def width(self) -> int:
        return len(self._grid[0])

    @property
    def height(self) -> int:
        return len(self._grid)

    def in_bounds(self, id: GridLocation) -> bool:
        x, y = id
        return 0 <= x < self.width and 0 <= y < self.height

    def __iter__(self) -> Iterator[list[T]]:
        return iter(self._grid)

    def __getitem__(self, loc: GridLocation) -> T:
        x, y = loc
        return self._grid[y][x]

    def neighbours(self, loc: GridLocation) -> Iterable[GridLocation]:
        x, y = loc
        neighbours = [
            (x + 1, y),
            (x + 1, y + 1),
            (x, y + 1),
            (x - 1, y + 1),
            (x - 1, y),
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
        ]

        for loc in neighbours:
            if self.in_bounds(loc):
                yield loc

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._grid)


@register(day=3)
def solve(file: IO[str], verbose: int) -> None:
    grid = Grid([[c for c in line.rstrip()] for line in file])
    part_numbers = []
    width = grid.width
    gear_numbers: defaultdict[GridLocation, list[int]] = defaultdict(list)
    for y, row in enumerate(grid):
        number_chars = []
        is_part = False
        cogs: set[GridLocation] = set()
        for x, char in enumerate(row):
            isdigit = char.isdigit()
            if isdigit:
                number_chars.append(char)
                for loc in grid.neighbours((x, y)):
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
