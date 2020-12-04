#! /usr/bin/env python3

from functools import reduce
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-03.txt").read_text()

# part 1
lines = text.split("\n")


def trees_for_slope(dx: int, dy: int, lines: list) -> int:
    x = 0
    y = 0
    # dx = 3
    # dy = 1
    count = 0
    while y < len(lines):
        if lines[y][x] == '#':
            count += 1
        x += dx
        x %= len(lines[0])
        y += dy

    return count


trees = trees_for_slope(3, 1, lines)

print(f"Encountered {trees} trees.")

# part2
slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

counts = []
for dx, dy in slopes:
    counts.append(trees_for_slope(dx, dy, lines))

print(f"Encountered {counts} trees.")
product = reduce(lambda x, y: x * y, counts, 1)
print(f"Product is {product}.")
