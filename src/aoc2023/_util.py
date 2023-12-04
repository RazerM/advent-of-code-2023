from collections import deque
from collections.abc import Iterable, Iterator
from typing import cast, overload


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
