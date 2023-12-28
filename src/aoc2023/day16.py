from typing import IO

from ._registry import register
from ._rust.day16 import Direction, fire_laser, max_edge_energized
from ._util import Grid, Vector


@register(day=16)
def solve(file: IO[str], verbose: int) -> None:
    grid = Grid([list(line.rstrip()) for line in file])

    print("Part 1:", fire_laser(grid, Vector(0, 0), Direction.RIGHT))
    print("Part 2:", max_edge_energized(grid))
