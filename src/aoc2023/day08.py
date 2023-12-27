import math
import re
from collections.abc import Sequence
from itertools import cycle
from typing import IO, Literal, assert_never, cast

from ._registry import register


@register(day=8)
def solve(file: IO[str], verbose: int) -> None:
    instructions = cast("Sequence[Literal['L', 'R']]", next(file).rstrip())
    node_map: dict[str, tuple[str, str]] = dict()
    for line in file:
        line = line.rstrip()
        if not line:
            continue
        match = re.match(r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)", line)
        assert match is not None, line
        node, left, right = match.groups()
        node_map[node] = left, right

    def steps(node):
        step = 0
        for step, instruction in enumerate(cycle(instructions)):
            if node.endswith("Z"):
                break
            match instruction:
                case "L":
                    node = node_map[node][0]
                case "R":
                    node = node_map[node][1]
                case _:
                    assert_never(instruction)
        return step

    print("Part 1:", steps("AAA"))

    nodes = [node for node in node_map if node.endswith("A")]

    print("Part 2:", math.lcm(*(steps(node) for node in nodes)))
