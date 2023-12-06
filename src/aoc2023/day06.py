import math
from typing import IO
from numpy.polynomial import Polynomial

from ._registry import register


def num_wins(time: int, record_distance: int) -> int:
    # charge_time + travel_time = time
    # speed = charge_time
    #
    # travel_time = time - charge_time
    #
    # distance = speed * travel_time
    # => distance = charge_time * travel_time
    # => distance = charge_time * (time - charge_time)
    # => distance = charge_time*time - charge_time**2
    # => -charge_time**2 + time*charge_time - distance
    #
    # find the roots of this polynomial where the distance beats the record
    poly = Polynomial([-(record_distance + 1), time, -1])
    c1, c2 = poly.roots()
    # We know that all charge times within are wins, so we can count how many
    first_win = math.ceil(c1)
    last_win = math.floor(c2)
    return last_win - first_win + 1


@register(day=6)
def solve(file: IO[str], verbose: int) -> None:
    line_t, line_d = file

    times = [int(s) for s in line_t.removeprefix("Time:").strip().split()]
    distances = [int(s) for s in line_d.removeprefix("Distance:").strip().split()]

    print("Part 1:", math.prod(num_wins(t, r) for t, r in zip(times, distances)))

    time = int(line_t.removeprefix("Time:").replace(" ", ""))
    distance = int(line_d.removeprefix("Distance:").replace(" ", ""))

    print("Part 2:", num_wins(time, distance))
