import math
from typing import IO

from ._registry import register
from ._rust.day02 import Colour, parse_game


@register(day=2)
def solve(file: IO[str], verbose: int) -> None:
    cubes = {Colour.RED: 12, Colour.GREEN: 13, Colour.BLUE: 14}
    empty = {Colour.RED: 0, Colour.GREEN: 0, Colour.BLUE: 0}

    game_powers = []
    possible_games = set()
    for line in file:
        game = parse_game(line)

        min_required = empty.copy()
        valid = True
        for set_ in game.sets:
            hand = empty.copy()
            for num, colour in set_:
                if cubes[colour] < num:
                    valid = False
                hand[colour] += num

            for colour, num in hand.items():
                min_required[colour] = max(min_required[colour], num)

        if valid:
            possible_games.add(game.id)
        game_powers.append(math.prod(min_required.values()))

    print("Part 1:", sum(possible_games))
    print("Part 2:", sum(game_powers))
