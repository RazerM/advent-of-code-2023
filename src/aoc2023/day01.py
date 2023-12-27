import re
from collections.abc import Iterable, Iterator
from typing import IO

from ._registry import register
from ._util import last

digit_words = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

re_digit_words = re.compile(f"({'|'.join(digit_words)})")


def digits(s: str, /, *, words: bool = False) -> Iterator[str]:
    for i in range(len(s)):
        if s[i].isdigit():
            yield s[i]
        elif words and (match := re_digit_words.match(s[i:])):
            yield digit_words[match[1]]


def first_last[T](iterable: Iterable[T]) -> tuple[T, T]:
    iterator = iter(iterable)
    first = next(iterator)
    return first, last(iterator, default=first)


@register(day=1)
def solve(file: IO[str], verbose: int) -> None:
    lines = file.readlines()
    total = 0
    for line in lines:
        value = int("".join(first_last(digits(line))))
        total += value
    print("Part 1:", total)

    total = 0
    for line in lines:
        value = int("".join(first_last(digits(line, words=True))))
        total += value
    print("Part 2:", total)
