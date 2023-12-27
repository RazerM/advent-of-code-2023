from collections import Counter
from enum import Enum, auto
from functools import total_ordering
from typing import IO, NamedTuple

from ._registry import register

type AnyCard = Card | CardJokerVariant
type Hand = tuple[AnyCard, AnyCard, AnyCard, AnyCard, AnyCard]


@total_ordering
class Card(Enum):
    _sort_value: int

    TWO = ("2", auto())
    THREE = ("3", auto())
    FOUR = ("4", auto())
    FIVE = ("5", auto())
    SIX = ("6", auto())
    SEVEN = ("7", auto())
    EIGHT = ("8", auto())
    NINE = ("9", auto())
    TEN = ("T", auto())
    JACK = ("J", auto())
    QUEEN = ("Q", auto())
    KING = ("K", auto())
    ACE = ("A", auto())

    def __new__(cls, character, sort_value):
        instance = object.__new__(cls)
        instance._value_ = character
        instance._sort_value = sort_value
        return instance

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self._sort_value < other._sort_value


@total_ordering
class CardJokerVariant(Enum):
    _sort_value: int

    JOKER = ("J", auto())
    TWO = ("2", auto())
    THREE = ("3", auto())
    FOUR = ("4", auto())
    FIVE = ("5", auto())
    SIX = ("6", auto())
    SEVEN = ("7", auto())
    EIGHT = ("8", auto())
    NINE = ("9", auto())
    TEN = ("T", auto())
    QUEEN = ("Q", auto())
    KING = ("K", auto())
    ACE = ("A", auto())

    def __new__(cls, character, sort_value):
        instance = object.__new__(cls)
        instance._value_ = character
        instance._sort_value = sort_value
        return instance

    def __lt__(self, other):
        if not isinstance(other, CardJokerVariant):
            return NotImplemented
        return self._sort_value < other._sort_value


@total_ordering
class HandType(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

    def __lt__(self, other):
        if not isinstance(other, HandType):
            return NotImplemented
        return self.value < other.value


class HandBid(NamedTuple):
    cards: Hand
    bid: int


def is_five_of_a_kind(hand: Hand):
    unique = set(hand)
    unique.discard(CardJokerVariant.JOKER)
    return len(unique) <= 1


def is_joker(card: AnyCard) -> bool:
    return card is CardJokerVariant.JOKER


def is_four_of_a_kind(hand: Hand) -> bool:
    counts = Counter(hand)
    num_jokers = counts[CardJokerVariant.JOKER]
    num_other = next(
        (num for card, num in counts.most_common() if not is_joker(card)), 0
    )
    return num_jokers + num_other == 4


def is_full_house(hand: Hand) -> bool:
    counts = Counter(hand)
    num_jokers = counts[CardJokerVariant.JOKER]
    most_common = (num for card, num in counts.most_common() if not is_joker(card))
    three_num = next(most_common, 0)
    if three_num <= 3 <= three_num + num_jokers:
        num_jokers -= 3 - three_num
    else:
        return False
    two_num = next(most_common, 0)
    return two_num + num_jokers == 2


def is_three_of_a_kind(hand: Hand) -> bool:
    counts = Counter(hand)
    num_jokers = counts[CardJokerVariant.JOKER]
    most_common = (num for card, num in counts.most_common() if not is_joker(card))
    num_other = next(most_common, 0)
    return num_jokers + num_other == 3 and next(most_common, 0) < 2


def is_two_pair(hand: Hand) -> bool:
    counts = Counter(hand)
    num_jokers = counts[CardJokerVariant.JOKER]
    most_common = (num for card, num in counts.most_common() if not is_joker(card))
    first_pair_num = next(most_common, 0)
    if first_pair_num <= 2 <= first_pair_num + num_jokers:
        num_jokers -= 2 - first_pair_num
    else:
        return False
    second_pair_num = next(most_common, 0)
    return second_pair_num + num_jokers == 2


def is_one_pair(hand: Hand) -> bool:
    counts = Counter(hand)
    num_jokers = counts[CardJokerVariant.JOKER]
    most_common = (num for card, num in counts.most_common() if not is_joker(card))
    num_other = next(most_common, 0)
    return num_jokers + num_other == 2 and next(most_common, 0) < 2


def hand_type(hand: Hand) -> HandType:
    assert len(hand) == 5
    counts = Counter(hand)
    most_common = counts.most_common()
    if is_five_of_a_kind(hand):
        return HandType.FIVE_OF_A_KIND
    elif is_four_of_a_kind(hand):
        return HandType.FOUR_OF_A_KIND
    elif is_full_house(hand):
        return HandType.FULL_HOUSE
    elif is_three_of_a_kind(hand):
        return HandType.THREE_OF_A_KIND
    elif is_two_pair(hand):
        return HandType.TWO_PAIR
    elif is_one_pair(hand):
        return HandType.ONE_PAIR
    else:
        return HandType.HIGH_CARD


def parse(line: str) -> tuple[str, int]:
    cards, bid = line.rstrip().split()
    return cards, int(bid)


def calulate_winnings(parsed: list[tuple[str, int]], card_cls: type[AnyCard]) -> int:
    hands: list[HandBid] = []
    for cards, bid in parsed:
        hands.append(HandBid(tuple(card_cls(c) for c in cards), bid))

    hands.sort(key=lambda h: h.cards, reverse=False)
    hands.sort(key=lambda h: hand_type(h.cards))
    total = 0
    for rank, hand in enumerate(hands, start=1):
        total += hand.bid * rank
    return total


@register(day=7)
def solve(file: IO[str], verbose: int) -> None:
    parsed = [parse(line) for line in file]
    print("Part 1:", calulate_winnings(parsed, Card))
    print("Part 2:", calulate_winnings(parsed, CardJokerVariant))
