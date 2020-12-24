#! /usr/bin/env python3

from collections import defaultdict, deque, namedtuple, Counter
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-24.txt").read_text()
lines = text.split("\n")
lines = [line.replace("se", "1").replace("sw", "2").replace("nw", "3").replace("ne", "4") for line in lines]


# part 1
deltas = {
    "e": lambda x, y: (1, 0),
    "1": lambda x, y: (1 if y & 1 == 1 else 0, -1),     # se
    "2": lambda x, y: (-1 if y & 1 == 0 else 0, -1),    # sw
    "w": lambda x, y: (-1, 0),
    "3": lambda x, y: (-1 if y & 1 == 0 else 0, 1),     # nw
    "4": lambda x, y: (1 if y & 1 == 1 else 0, 1)       # ne
}

def trace(directions: str) -> tuple:

    x = 0
    y = 0
    for direction in directions:
        dx, dy = deltas[direction](x, y)
        x += dx
        y += dy

    return x, y


def layout(lines: list) -> dict:

    tiles = defaultdict(int)    # 0 - white, ~0 - black
    for line in lines:
        x, y = trace(line)
        tiles[(x, y)] = ~tiles[(x, y)]

    return tiles


tiles = layout(lines)
counts = Counter(tiles.values())
print(f"# of black tiles = {counts[-1]}")


# part 2
def check(x: int, y: int, tiles: dict) -> int:
    count = 0
    dx, dy = deltas["e"](x, y)
    count += 1 if tiles[(x+dx, y+dy)] != 0 else 0
    dx, dy = deltas["1"](x, y)
    count += 1 if tiles[(x+dx, y+dy)] != 0 else 0
    dx, dy = deltas["2"](x, y)
    count += 1 if tiles[(x+dx, y+dy)] != 0 else 0
    dx, dy = deltas["w"](x, y)
    count += 1 if tiles[(x+dx, y+dy)] != 0 else 0
    dx, dy = deltas["3"](x, y)
    count += 1 if tiles[(x+dx, y+dy)] != 0 else 0
    dx, dy = deltas["4"](x, y)
    count += 1 if tiles[(x+dx, y+dy)] != 0 else 0
    return count


def day(tiles: dict) -> dict:

    black = [coord for coord in tiles.keys() if tiles[coord] != 0]
    # dilate by one to consider white tiles around black tiles
    minx = min([coord[0] for coord in black]) - 1
    maxx = max([coord[0] for coord in black]) + 1
    miny = min([coord[1] for coord in black]) - 1
    maxy = max([coord[1] for coord in black]) + 1
    flip = []
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            count = check(x, y, tiles)
            if tiles[(x, y)] != 0 and (count == 0 or count > 2):
                flip.append((x, y))
            elif tiles[(x, y)] == 0 and count == 2:
                flip.append((x, y))
    for tile in flip:
        tiles[tile] = ~tiles[tile]

    return tiles


for _ in range(100):
    tiles = day(tiles)

counts = Counter(tiles.values())
print(f"# of black tiles = {counts[-1]}")   # !377, !619, +3831

print(".oO( done )")
