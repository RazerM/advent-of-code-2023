from collections.abc import Iterable, Iterator
from functools import lru_cache
from typing import IO

from ._registry import register

type Springs = str
type Groups = tuple[int, ...]
type Record = tuple[Springs, Groups]


@lru_cache
def arrangements(springs: Springs, groups: Groups) -> int:
    if not springs:
        if groups:
            # expecting another group, but no input left
            return 0
        else:
            # we've consumed all springs and have no groups left, this is a
            # valid arrangement
            return 1

    if not groups:
        # valid arrangement as long as there are no damaged springs left
        return 0 if "#" in springs else 1

    count = 0

    # Operational or treat unknown as operational
    if springs[0] in {".", "?"}:
        # Since we're looking for groups of damaged springs, we can strip
        # off this spring and continue the search
        count += arrangements(springs[1:], groups)

    # Damaged or treat unknown as damaged
    if springs[0] in {"#", "?"}:
        group = groups[0]

        if (
            len(springs) >= group
            and "." not in springs[:group]
            and (len(springs) == group or springs[group] != "#")
        ):
            count += arrangements(springs[group + 1 :], groups[1:])

    return count


def parse(lines: Iterable[str]) -> Iterator[Record]:
    for line in lines:
        springs, groups = line.rstrip().split()
        yield springs, tuple(int(num) for num in groups.split(","))


def unfold(record: Record, *, folds: int) -> Record:
    springs, groups = record
    return "?".join([springs] * folds), groups * folds


def count_arrangements(records: Iterable[Record]) -> int:
    return sum(arrangements(springs, numbers) for springs, numbers in records)


@register(day=12)
def solve(file: IO[str], verbose: int) -> None:
    records = list(parse(file))

    print("Part 1:", count_arrangements(records))

    unfolded = [unfold(r, folds=5) for r in records]
    print("Part 2:", count_arrangements(unfolded))
