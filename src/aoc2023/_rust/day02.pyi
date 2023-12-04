from typing import ClassVar

class Colour:
    Red: ClassVar[Colour]
    Green: ClassVar[Colour]
    Blue: ClassVar[Colour]

class Game:
    id: int
    sets: list[list[tuple[int, Colour]]]

def parse_game(input: str) -> Game: ...
