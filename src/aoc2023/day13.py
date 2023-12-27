from collections.abc import Iterator
from typing import IO

from ._registry import register


def rotate(lines: list[str]) -> list[str]:
    """Rotate a list of lines by 90 degrees anti-clockwise

    ABCDE
    12345

    becomes

    E5
    D4
    C3
    B2
    A1
    """
    return ["".join(col) for col in reversed(list(zip(*lines)))]


def mirrored(block: list[str]) -> Iterator[tuple[int, int]]:
    """Yield (position, num_errors) tuples where lines are mirrored."""
    width = len(block[0])
    for x in range(1, width):
        total_errors = 0
        for line in block:
            short, long = sorted([line[:x], line[x:]], key=len)
            meth = endswith_lenient if x > width / 2 else startswith_lenient

            match, errors = meth(long, short[::-1])
            if not match:
                break
            total_errors += errors
        else:
            yield x, total_errors


def endswith_lenient(s: str, suffix: str) -> tuple[bool, int]:
    """str.endswith but allows up to one error."""
    if len(s) < len(suffix):
        return False, 0

    errors = 0
    for a, b in zip(s[-len(suffix) :], suffix, strict=True):
        if a != b:
            errors += 1

    if errors <= 1:
        return True, errors
    else:
        return False, 0


def startswith_lenient(s: str, prefix: str) -> tuple[bool, int]:
    """str.endswith but allows up to one error."""
    if len(s) < len(prefix):
        return False, 0

    errors = 0
    for a, b in zip(s, prefix):
        if a != b:
            errors += 1

    if errors <= 1:
        return True, errors
    else:
        return False, 0


@register(day=13)
def solve(file: IO[str], verbose: int) -> None:
    blocks: list[list[str]] = []
    block: list[str] = []
    for line in file:
        line = line.rstrip()
        if not line:
            blocks.append(block)
            block = []
        else:
            block.append(line)

    if block:
        blocks.append(block)

    checksum = 0
    smudge_checksum = 0
    for i, block in enumerate(blocks):
        for x, errors in mirrored(block):
            if errors == 0:
                checksum += x
            elif errors == 1:
                smudge_checksum += x

        for y, errors in mirrored(rotate(block)):
            if errors == 0:
                checksum += 100 * y
            elif errors == 1:
                smudge_checksum += 100 * y

    print("Part 1:", checksum)
    print("Part 2:", smudge_checksum)
