from collections import deque
from collections.abc import Collection
from enum import Enum
from typing import IO

from ._registry import register
from ._util import Grid, Vector


class Tile(Enum):
    VERTICAL = "|"
    HORIZONTAL = "-"
    NORTH_EAST = "L"
    NORTH_WEST = "J"
    SOUTH_WEST = "7"
    SOUTH_EAST = "F"
    GROUND = "."
    START = "S"

    def __str__(self) -> str:
        return self.value


start_tiles: dict[tuple[bool, bool, bool, bool], Tile] = {
    (True, True, False, False): Tile.NORTH_EAST,
    (True, False, True, False): Tile.VERTICAL,
    (True, False, False, True): Tile.NORTH_WEST,
    (False, True, True, False): Tile.SOUTH_EAST,
    (False, True, False, True): Tile.HORIZONTAL,
    (False, False, True, True): Tile.SOUTH_WEST,
}

NORTH = Vector(0, -1)
EAST = Vector(1, 0)
SOUTH = Vector(0, 1)
WEST = Vector(-1, 0)

directions = {
    Tile.VERTICAL: [NORTH, SOUTH],
    Tile.HORIZONTAL: [EAST, WEST],
    Tile.NORTH_EAST: [NORTH, EAST],
    Tile.NORTH_WEST: [NORTH, WEST],
    Tile.SOUTH_WEST: [SOUTH, WEST],
    Tile.SOUTH_EAST: [SOUTH, EAST],
    Tile.GROUND: [],
}


def inside_shape(
    grid: Grid[Tile], shape: Collection[Vector[int]], point: Vector[int]
) -> bool:
    """Crossing number algorithm"""
    if point in shape:
        return False

    diag = Vector(1, 1)
    glancing_corners = {Tile.SOUTH_WEST, Tile.NORTH_EAST}

    crosses = 0
    while grid.in_bounds(point):
        if point in shape and grid[point] not in glancing_corners:
            crosses += 1
        point += diag

    return crosses % 2 == 1


@register(day=10)
def solve(file: IO[str], verbose: int) -> None:
    grid = Grid([[Tile(c) for c in line.rstrip()] for line in file])
    start: Vector[int] | None = None
    graph: dict[Vector[int], set[Vector[int]]] = dict()
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            pos = Vector(x, y)
            if tile is Tile.START:
                north = pos + NORTH
                east = pos + EAST
                south = pos + SOUTH
                west = pos + WEST
                connects_north = grid[north] in {
                    Tile.VERTICAL,
                    Tile.SOUTH_EAST,
                    Tile.SOUTH_WEST,
                }
                connects_east = grid[east] in {
                    Tile.HORIZONTAL,
                    Tile.NORTH_WEST,
                    Tile.SOUTH_WEST,
                }
                connects_south = grid[south] in {
                    Tile.VERTICAL,
                    Tile.NORTH_EAST,
                    Tile.NORTH_WEST,
                }
                connects_west = grid[west] in {
                    Tile.HORIZONTAL,
                    Tile.NORTH_EAST,
                    Tile.SOUTH_EAST,
                }

                start = pos
                grid[pos] = start_tiles[
                    connects_north, connects_east, connects_south, connects_west
                ]

            graph[pos] = {pos + direction for direction in directions[grid[pos]]}

    seen: set[Vector[int]] = set()
    assert start is not None
    queue = deque([start])

    while queue:
        pos = queue.popleft()
        for neighbour in graph[pos]:
            if neighbour not in seen:
                queue.append(neighbour)
                seen.add(neighbour)

    print("Part 1:", len(seen) // 2)

    inside = 0
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            pos = Vector(x, y)
            if pos in seen:
                continue

            if inside_shape(grid, seen, pos):
                inside += 1

    print("Part 2:", inside)
