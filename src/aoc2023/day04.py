from functools import cached_property
from typing import IO

import regex
from attrs import define, field

from ._registry import register


@define(slots=False)
class Card:
    id: int
    winning: frozenset[int] = field(converter=frozenset)
    mine: frozenset[int] = field(converter=frozenset)
    quantity: int = 1

    @cached_property
    def matching(self) -> int:
        return len(self.winning & self.mine)

    @cached_property
    def points(self) -> int:
        if not self.matching:
            return 0

        return 2 ** (self.matching - 1)


@register(day=4)
def solve(file: IO[str], verbose: int) -> None:
    cards: dict[int, Card] = {}

    for line in file:
        match = regex.match(
            r"""
            Card\s+(?P<id>\d+):\s*                    # Card <id>
            (?P<winning>\d+)(?:\s+(?P<winning>\d+))*  # winning numbers
            \s*\|\s*                                  # separator
            (?P<mine>\d+)(?:\s+(?P<mine>\d+))*        # my numbers
            \s*
            """,
            line,
            regex.VERBOSE,
        )
        winning = [int(s) for s in match.captures("winning")]
        mine = [int(s) for s in match.captures("mine")]
        card_id = int(match["id"])
        cards[card_id] = Card(card_id, winning, mine)

    print("Part 1:", sum(card.points for card in cards.values()))

    for card in cards.values():
        for win_id in range(card.id + 1, card.id + 1 + card.matching):
            cards[win_id].quantity += cards[card.id].quantity

    print("Part 2:", sum(card.quantity for card in cards.values()))
