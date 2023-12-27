from collections.abc import Iterator
from itertools import combinations
from typing import IO

from ._registry import register
from ._util import Grid, Vector


def between(a: int, b: int) -> Iterator[int]:
    if b < a:
        a, b = b, a
    return iter(range(a, b + 1))


@register(day=11)
def solve(file: IO[str], verbose: int) -> None:
    grid = Grid([list(line.rstrip()) for line in file])
    empty_rows = {y for y, row in enumerate(grid.rows()) if all(c == "." for c in row)}
    empty_cols = {
        x for x, col in enumerate(grid.columns()) if all(c == "." for c in col)
    }

    galaxies = set()
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            pos = Vector(x, y)
            if tile == "#":
                galaxies.add(pos)

    def distances(*, expansion: int = 2) -> Iterator[int]:
        for a, b in combinations(galaxies, 2):
            yield (
                abs(a.x - b.x)
                + abs(a.y - b.y)
                + len(empty_cols & set(between(a.x, b.x))) * (expansion - 1)
                + len(empty_rows & set(between(a.y, b.y))) * (expansion - 1)
            )

    print("Part 1:", sum(distances()))
    print("Part 2:", sum(distances(expansion=1000000)))
