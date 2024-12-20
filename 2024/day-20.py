from pathlib import Path
# import re

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "day-20.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "###############",
#     "#...#...#.....#",
#     "#.#.#.#.#.###.#",
#     "#S#...#.#.#...#",
#     "#######.#.#.###",
#     "#######.#.#...#",
#     "#######.#.###.#",
#     "###..E#...#...#",
#     "###.#######.###",
#     "#...###...#...#",
#     "#.#####.#.###.#",
#     "#.#...#.#.#...#",
#     "#.#.#.#.#.#.###",
#     "#...#...#...###",
#     "###############",
# ]

width = len(lines[0])
height = len(lines)
course = np.array([list(map(ord, line)) for line in lines], dtype=np.uint8)
steps = np.full((height, width), -1, dtype=np.int32)

WALL = ord("#")
OPEN = ord(".")
START = ord("S")
END = ord("E")

ys, xs = np.where(course == START)
sx, sy = xs[0], ys[0]
ys, xs = np.where(course == END)
ex, ey = xs[0], ys[0]

count = 0
x, y = sx, sy
while (x, y) != (ex, ey):
    steps[y, x] = count
    if steps[y-1, x] == -1 and course[y-1, x] != WALL:
        y -= 1
    elif steps[y, x+1] == -1 and course[y, x+1] != WALL:
        x += 1
    elif steps[y+1, x] == -1 and course[y+1, x] != WALL:
        y += 1
    elif steps[y, x-1] == -1 and course[y, x-1] != WALL:
        x -= 1
    else:
        raise RuntimeError("No path found!")
    count += 1

steps[y, x] = count

print(f"Steps: {steps[sy, sx]=}")
print(f"Steps: {steps[ey, ex]=}")

cheats = []
for y in range(1, height-1):
    for x in range(1, width-1):
        if course[y, x] != WALL:
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                wx, wy = x + dx, y + dy
                tx, ty = x + 2*dx, y + 2*dy
                if 0 <= tx < width and 0 <= ty < height and \
                    course[wy, wx] == WALL and course[ty, tx] != WALL:
                    if steps[ty, tx] > steps[y, x]:
                        # print(f"{(x,y)=} -> {(tx, ty)=} {steps[y, x]=} -> {steps[ty, tx]=}")
                        cheats.append((wx, wy, tx, ty, steps[ty, tx] - steps[y, x] - 2))

from collections import defaultdict
counts = defaultdict(list)

for wx, wy, tx, ty, savings in cheats:
    counts[savings].append((wx, wy, tx, ty))

if height == 15 and width == 15:
    for count in sorted(counts.keys()):
        print(f"{len(counts[count])} cheats save {count} picoseconds")

total = 0
for count in counts:
    if count >= 100:
        total += len(counts[count])

print(f"Total: {total=}")

counts = defaultdict(lambda: 0)
bigger = np.full((height+42, width+42), WALL, dtype=np.uint8)
bigger[21:21+height, 21:21+width] = course
for y in range(1, course.shape[0]-1):
    yp = y + 21
    for x in range(1, course.shape[1]-1):
        xp = x + 21
        if bigger[yp, xp] == WALL:
            continue
        for dy in range(-20, 21):
            for dx in range(-20, 21):
                distance = abs(dx) + abs(dy)
                if distance > 20:
                    continue
                # if dx == 0 and dy == 0:
                #     continue
                if bigger[yp+dy, xp+dx] == WALL:
                    continue
                if steps[y+dy, x+dx] > (steps[y, x] + distance):
                    cheat = steps[y+dy, x+dx] - steps[y, x] - distance
                    counts[cheat] += 1

if height == 15 and width == 15:
    for count in sorted(counts.keys()):
        if count >= 50:
            print(f"{counts[count]} cheats save {count} picoseconds")

total = 0
for count in counts:
    if count >= 100:
        total += counts[count]

print(f"Total: {total=}")


print("Done!")
