from collections import deque
from itertools import pairwise
from typing import IO

from ._registry import register


def extrapolate(history, *, backwards: bool = False):
    stack = deque([history])
    while any(top := stack[-1]):
        stack.append(deque(b - a for a, b in pairwise(top)))
    last = None
    while stack:
        top = stack.pop()
        if last is None:
            if backwards:
                top.appendleft(0)
            else:
                top.append(0)
        else:
            if backwards:
                top.appendleft(top[0] - last[0])
            else:
                top.append(top[-1] + last[-1])
        last = top

    assert last is not None
    return last[0] if backwards else last[-1]


@register(day=9)
def solve(file: IO[str], verbose: int) -> None:
    histories = []
    for line in file:
        line = line.rstrip()
        history = deque(int(s) for s in line.split())
        histories.append(history)

    print("Part 1:", sum(extrapolate(h) for h in histories))
    print("Part 2:", sum(extrapolate(h, backwards=True) for h in histories))
