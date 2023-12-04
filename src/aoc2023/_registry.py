from collections.abc import Callable
from typing import IO, Protocol


class Solver(Protocol):
    def __call__(self, file: IO[str], verbose: int) -> None:
        ...


solvers: dict[int, Solver] = dict()


def register(*, day: int) -> Callable[[Solver], Solver]:
    def decorator(fn: Solver) -> Solver:
        if day in solvers:
            raise ValueError(f"Day {day} is already registered")
        solvers[day] = fn
        return fn

    return decorator
