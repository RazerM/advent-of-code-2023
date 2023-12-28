from typing import ClassVar

class Colour:
    RED: ClassVar[Colour]
    GREEN: ClassVar[Colour]
    BLUE: ClassVar[Colour]

class Game:
    id: int
    sets: list[list[tuple[int, Colour]]]

def parse_game(input: str) -> Game: ...
