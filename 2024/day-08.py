from pathlib import Path

# import numpy as np

with (Path(__file__).parent / "day-08.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "............",
#     "........0...",
#     ".....0......",
#     ".......0....",
#     "....0.......",
#     "......A.....",
#     "............",
#     "............",
#     "........A...",
#     ".........A..",
#     "............",
#     "............",
# ]

from collections import defaultdict
from collections import namedtuple

Pos = namedtuple("Pos", ["x", "y"])

nodes = defaultdict(list)
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char != ".":
            nodes[char].append(Pos(x, y))

from itertools import combinations

height = len(lines)
width = len(lines[0])

antinodes = set()
for antenna, positions in nodes.items():
    # print("antenna = {antenna}")
    for combination in combinations(positions, 2):
        # print(f"\t{combination}")
        one, two = list(combination)
        if one.y > two.y:
            one, two = two, one
        elif one.x > two.x:
            one, two = two, one
        dx = two.x - one.x
        dy = two.y - one.y
        antinode1 = Pos(one.x - dx, one.y - dy)
        antinode2 = Pos(two.x + dx, two.y + dy)
        if (0 <= antinode1.x) and (antinode1.x < width) and (0 <= antinode1.y) and (antinode1.y < height):
            antinodes.add(antinode1)
        if (0 <= antinode2.x) and (antinode2.x < width) and (0 <= antinode2.y) and (antinode2.y < height):
            antinodes.add(antinode2)

print(f"# of unique antinodes = {len(antinodes)}")

for antenna, positions in nodes.items():
    for combination in combinations(positions, 2):
        one, two = list(combination)
        if one.y > two.y:
            one, two = two, one
        elif one.x > two.x:
            one, two = two, one
        dx = two.x - one.x
        dy = two.y - one.y
        x, y = one
        while (0 <= x) and (x < width) and (0 <= y) and (y < height):
            antinodes.add(Pos(x, y))
            x -= dx
            y -= dy
        x, y = two
        while (0 <= x) and (x < width) and (0 <= y) and (y < height):
            antinodes.add(Pos(x, y))
            x += dx
            y += dy

print(f"# of unique antinodes = {len(antinodes)}")

print("Done.")
