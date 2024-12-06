from pathlib import Path
import re

import numpy as np

with (Path(__file__).parent / "day-06.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

"""
lines = [
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#..^.....",
    "........#.",
    "#.........",
    "......#...",
]
"""

mahp = np.array([list(map(ord, list(line))) for line in lines])
pos = np.nonzero(mahp == ord("^"))
x0 = pos[1][0]
y0 = pos[0][0]

rotate = {
    (0, -1): (1, 0),
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1)
}

visited = set()
x, y = x0, y0
dx, dy = 0, -1
while True:
    visited.add((x,y))
    xp, yp = x + dx, y + dy
    if (xp >= 0) and (xp < mahp.shape[1]) and (yp >= 0) and (yp < mahp.shape[0]):
        if mahp[yp, xp] == ord("#"):
            dx, dy = rotate[(dx, dy)]
        else:
            x, y = xp, yp
    else:
        break

print(f"Num visited = {len(visited)}")

def loops(x, y, dx, dy):
    visited = set()
    while True:
        if (x, y, dx, dy) in visited:
            return True
        xp, yp = x + dx, y + dy
        if (xp >= 0) and (xp < mahp.shape[1]) and (yp >= 0) and (yp < mahp.shape[0]):
            if mahp[yp, xp] == ord("#"):
                dx, dy = rotate[(dx, dy)]
            else:
                visited.add((x,y,dx,dy))
                x, y = xp, yp
        else:
            return False

barriers = set()
x, y = x0, y0
dx, dy = 0, -1
while True:
    xp, yp = x + dx, y + dy
    if (xp >= 0) and (xp < mahp.shape[1]) and (yp >= 0) and (yp < mahp.shape[0]):
        if mahp[yp, xp] == ord("#"):
            dx, dy = rotate[(dx, dy)]
        else:
            if (x, y, dx, dy) != (x0, y0, 0, -1):
                mahp[yp, xp] = ord("#")
                if loops(x0, y0, 0, -1):
                    barriers.add((xp, yp))
                mahp[yp, xp] = ord(".")
            x, y = xp, yp
    else:
        break

# 1880 too low
# 2354 too high
print(f"Number of barrier positions: {len(barriers)}")


print("Done.")
