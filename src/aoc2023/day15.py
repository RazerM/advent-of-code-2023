import re
from collections import defaultdict
from typing import IO

from ._registry import register


def hash_algo(s: str) -> int:
    current = 0
    for c in s:
        current += ord(c)
        current *= 17
        current %= 256
    return current


@register(day=15)
def solve(file: IO[str], verbose: int) -> None:
    init_seq = next(file).rstrip().split(",")
    print("Part 1:", sum(hash_algo(step) for step in init_seq))

    boxes: defaultdict[int, dict[str, int]] = defaultdict(dict)
    for step in init_seq:
        match = re.match(r"^([a-z]+)([-=])([0-9]+)?$", step)
        assert match is not None
        label, op, digits = match.groups()

        box_num = hash_algo(label)
        box = boxes[box_num]
        match op:
            case "-":
                if label in box:
                    del box[label]
            case "=":
                assert digits is not None
                focal_length = int(digits)
                box[label] = focal_length

        if verbose >= 3:
            print(f'After "{step}":')
            for box_num, box in sorted(boxes.items()):
                if box:
                    print(
                        f"Box {box_num}:",
                        " ".join(
                            f"[{label} {focal_length}]"
                            for label, focal_length in box.items()
                        ),
                    )
            print()

    focusing_power = sum(
        (box_num + 1) * slot_num * focal_length
        for box_num, box in boxes.items()
        for slot_num, focal_length in enumerate(box.values(), start=1)
    )
    print("Part 2:", focusing_power)
