from collections import deque
from collections.abc import Mapping
from itertools import batched
from typing import IO

from ._registry import register


def map_int(source: int, source_dest_map: dict[range, range]) -> int:
    for source_range, dest_range in source_dest_map.items():
        if source in source_range:
            dest = source - source_range.start + dest_range.start
            break
    else:
        dest = source

    return dest


def range_overlap(a: range, b: range) -> bool:
    assert a.step == 1 and b.step == 1
    return a.start < b.stop and a.stop > b.start


def map_range(
    input_range: range, source_dest_map: Mapping[range, range]
) -> list[range]:
    for source_range, dest_range in source_dest_map.items():
        if range_overlap(input_range, source_range):
            offset = dest_range.start - source_range.start
            if (
                input_range.start >= source_range.start
                and input_range.stop <= source_range.stop
            ):
                return [range(input_range.start + offset, input_range.stop + offset)]
            elif input_range.start >= source_range.start:
                return [
                    range(input_range.start + offset, source_range.stop + offset),
                    *map_range(
                        range(source_range.stop, input_range.stop), source_dest_map
                    ),
                ]
            elif input_range.stop <= source_range.stop:
                return [
                    *map_range(
                        range(input_range.start, source_range.start), source_dest_map
                    ),
                    range(source_range.start + offset, input_range.stop + offset),
                ]
    else:
        return [input_range]


@register(day=5)
def solve(file: IO[str], verbose: int) -> None:
    graph: dict[str, str] = {}
    maps: dict[tuple[str, str], dict[range, range]] = {}

    current_map = None
    seeds: list[int] = []
    for line in file:
        line = line.rstrip()
        if line.startswith("seeds: "):
            seeds = [int(n) for n in line.removeprefix("seeds: ").split()]
        elif line.endswith(" map:"):
            map_name = line.removesuffix(" map:")
            source, dest = map_name.split("-to-", maxsplit=1)
            graph[source] = dest
            current_map = maps[source, dest] = dict()
        elif line:
            assert current_map is not None
            dest_start, source_start, length = map(int, line.split())
            current_map[range(source_start, source_start + length)] = range(
                dest_start, dest_start + length
            )

    locations = set()
    for item in seeds:
        source = "seed"
        while source != "location":
            dest = graph[source]
            item = map_int(item, maps[source, dest])
            source = dest
        locations.add(item)

    print("Part 1:", min(locations))

    seed_ranges = [range(start, start + length) for start, length in batched(seeds, 2)]

    location_ranges = set()
    queue: deque[tuple[str, range]] = deque(
        ("seed", seed_range) for seed_range in seed_ranges
    )
    while queue:
        source, item_range = queue.popleft()
        if source == "location":
            location_ranges.add(item_range)
        else:
            dest = graph[source]
            item_ranges = map_range(item_range, maps[source, dest])
            for item_range in item_ranges:
                queue.append((dest, item_range))

    print("Part 2:", min(r.start for r in location_ranges))
