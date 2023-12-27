from collections import defaultdict, deque
from copy import deepcopy
from enum import Enum, auto
from typing import IO

from ._registry import register
from ._util import Grid, Vector


class Direction(Enum):
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
    UP = auto()

    @property
    def vertical(self):
        return self in (Direction.DOWN, Direction.UP)

    @property
    def horizontal(self):
        return self in (Direction.LEFT, Direction.RIGHT)


MIRRORS = {
    "\\": {
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.RIGHT,
        Direction.LEFT: Direction.UP,
        Direction.UP: Direction.LEFT,
    },
    "/": {
        Direction.RIGHT: Direction.UP,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.DOWN,
        Direction.UP: Direction.RIGHT,
    },
}

MOVE = {
    Direction.RIGHT: Vector(1, 0),
    Direction.DOWN: Vector(0, 1),
    Direction.LEFT: Vector(-1, 0),
    Direction.UP: Vector(0, -1),
}

ARROWS = {
    Direction.RIGHT: ">",
    Direction.DOWN: "v",
    Direction.LEFT: "<",
    Direction.UP: "^",
}


def fire_laser(grid: Grid[str], pos: Vector[int], direction: Direction) -> int:
    queue = deque([(pos, direction)])
    energized: set[Vector[int]] = set()
    visited: defaultdict[Vector[int], set[Direction]] = defaultdict(set)

    while queue:
        pos, direction = queue.popleft()
        if not grid.in_bounds(pos):
            continue
        if direction in visited[pos]:
            continue
        visited[pos].add(direction)
        energized.add(pos)
        tile = grid[pos]
        match tile:
            case "\\" | "/":
                direction = MIRRORS[tile][direction]
                queue.append((pos + MOVE[direction], direction))
            case "|" if direction.horizontal:
                queue.append((pos + MOVE[Direction.UP], Direction.UP))
                queue.append((pos + MOVE[Direction.DOWN], Direction.DOWN))
            case "-" if direction.vertical:
                queue.append((pos + MOVE[Direction.LEFT], Direction.LEFT))
                queue.append((pos + MOVE[Direction.RIGHT], Direction.RIGHT))
            case _:
                queue.append((pos + MOVE[direction], direction))

    return len(energized)


@register(day=16)
def solve(file: IO[str], verbose: int) -> None:
    grid = Grid([list(line.rstrip()) for line in file])

    print("Part 1:", fire_laser(grid, Vector(0, 0), Direction.RIGHT))

    configurations = []
    for x in range(0, grid.width):
        configurations.append((Vector(x, 0), Direction.DOWN))
        configurations.append((Vector(x, grid.height - 1), Direction.UP))

    for y in range(0, grid.height):
        configurations.append((Vector(0, y), Direction.RIGHT))
        configurations.append((Vector(grid.width - 1, y), Direction.LEFT))

    print(
        "Part 2:",
        max(fire_laser(grid, pos, direction) for pos, direction in configurations),
    )
