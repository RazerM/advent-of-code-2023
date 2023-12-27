from collections import deque
from collections.abc import Iterable, Iterator
from typing import Self, cast, overload

from attrs import define


def tail[T](n: int, iterable: Iterable[T]) -> Iterator[T]:
    """Return an iterator over the last n items"""
    return iter(deque(iterable, maxlen=n))


class _Sentinel:
    pass


DEFAULT = _Sentinel()


@overload
def last[T](iterable: Iterable[T]) -> T:
    ...


@overload
def last[T](iterable: Iterable[T], *, default: T) -> T:
    ...


def last[T](iterable: Iterable[T], *, default: T | _Sentinel = DEFAULT) -> T:
    try:
        return next(tail(1, iterable))
    except StopIteration:
        if default is DEFAULT:
            raise
        return cast(T, default)


@define(frozen=True)
class Vector[T: (float, int)]:
    x: T
    y: T

    def __add__(self, other: Self) -> Self:
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        return NotImplemented

    def __sub__(self, other: Self) -> Self:
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

        return NotImplemented


class Grid[T]:
    def __init__(self, grid: list[list[T]]) -> None:
        self._grid = grid

    @property
    def width(self) -> int:
        return len(self._grid[0])

    @property
    def height(self) -> int:
        return len(self._grid)

    def in_bounds(self, loc: Vector[int]) -> bool:
        return 0 <= loc.x < self.width and 0 <= loc.y < self.height

    def __iter__(self) -> Iterator[list[T]]:
        return iter(self._grid)

    def __getitem__(self, loc: Vector[int]) -> T:
        return self._grid[loc.y][loc.x]

    def __setitem__(self, loc: Vector[int], value: T) -> None:
        self._grid[loc.y][loc.x] = value

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._grid)

    def neighbours(self, loc: Vector[int]) -> Iterable[Vector[int]]:
        neighbours = [
            Vector(loc.x + 1, loc.y),
            Vector(loc.x + 1, loc.y + 1),
            Vector(loc.x, loc.y + 1),
            Vector(loc.x - 1, loc.y + 1),
            Vector(loc.x - 1, loc.y),
            Vector(loc.x - 1, loc.y - 1),
            Vector(loc.x, loc.y - 1),
            Vector(loc.x + 1, loc.y - 1),
        ]

        for loc in neighbours:
            if self.in_bounds(loc):
                yield loc

    def rows(self) -> Iterator[Iterator[T]]:
        for row in self._grid:
            yield iter(row)

    def columns(self) -> Iterator[Iterator[T]]:
        for x in range(0, self.width):
            yield (self._grid[y][x] for y in range(0, self.height))
