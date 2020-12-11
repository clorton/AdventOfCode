#! /usr/bin/env python3

import numpy as np
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-11.txt").read_text()
rows = [list("." + line + ".") for line in text.split("\n")]
temp = [[] for _ in range(len(rows)+2)]
temp[0] = ["."]*len(rows[0])
temp[-1] = ["."]*len(rows[0])
for index, row in enumerate(rows):
    temp[index+1] = row


# part 1
FLOOR = ord(".")
SEAT = ord("L")
OCCUPIED = ord("#")


def update(state):
    counts = np.zeros(state.shape, dtype=np.uint8)
    tplus1 = np.zeros(state.shape, dtype=np.uint8)
    delta = 0
    height, width = state.shape
    for y in range(1, height-1):
        for x in range(1, width-1):
            if state[y, x] == FLOOR:
                continue
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dy == 0 and dx == 0:
                        continue
                    if state[y + dy, x + dx] == OCCUPIED:
                        counts[y, x] += 1
            if state[y, x] == SEAT and counts[y, x] == 0:
                tplus1[y, x] = OCCUPIED
                delta += 1
            elif state[y, x] == OCCUPIED and counts[y, x] >= 4:
                tplus1[y, x] = SEAT
                delta += 1
            else:
                tplus1[y, x] = state[y, x]
    return tplus1, delta


seating = np.zeros((len(temp), len(temp[0])))
for iy, row in enumerate(temp):
    for ix, entry in enumerate(row):
        seating[iy, ix] = ord(entry)

while True:
    seating, changes = update(seating)
    if changes == 0:
        break

print(f"{np.count_nonzero(seating == OCCUPIED)} seats are occupied")


# part 2
NORTH = 0
NORTHEAST = 1
EAST = 2
SOUTHEAST = 3
SOUTH = 4
SOUTHWEST = 5
WEST = 6
NORTHWEST = 7

deltas = {
    # dy, dx
    NORTH: (-1, 0),
    NORTHEAST: (-1, 1),
    EAST: (0, 1),
    SOUTHEAST: (1, 1),
    SOUTH: (1, 0),
    SOUTHWEST: (1, -1),
    WEST: (0, -1),
    NORTHWEST: (-1, -1)
}


def update2(state):
    count = np.zeros(state.shape, dtype=np.uint8)
    tplus1 = np.zeros(state.shape, dtype=np.uint8) + FLOOR
    height, width = state.shape
    delta = 0
    for y in range(1, height-1):
        for x in range(1, width-1):
            if state[y, x] == FLOOR:
                continue

            for direction, (dy, dx) in deltas.items():
                ytemp = y + dy
                xtemp = x + dx
                while 0 < ytemp < height-1 and 0 < xtemp < width - 1:
                    if state[ytemp, xtemp] == SEAT:
                        break
                    if state[ytemp, xtemp] == OCCUPIED:
                        count[y, x] += 1
                        break
                    ytemp += dy
                    xtemp += dx

            if state[y, x] == SEAT and count[y, x] == 0:
                tplus1[y, x] = OCCUPIED
                delta += 1
            elif state[y, x] == OCCUPIED and count[y, x] >= 5:
                tplus1[y, x] = SEAT
                delta += 1
            else:
                tplus1[y, x] = state[y, x]
    return tplus1, delta


"""
temp = [
    "............",
    ".L.LL.LL.LL.",
    ".LLLLLLL.LL.",
    ".L.L.L..L...",
    ".LLLL.LL.LL.",
    ".L.LL.LL.LL.",
    ".L.LLLLL.LL.",
    "...L.L......",
    ".LLLLLLLLLL.",
    ".L.LLLLLL.L.",
    ".L.LLLLL.LL.",
    "............"
]
"""

seating = np.zeros((len(temp), len(temp[0])), dtype=np.uint8)
for iy, row in enumerate(temp):
    for ix, entry in enumerate(row):
        seating[iy, ix] = ord(entry)

while True:
    seating, changes = update2(seating)
    # print()
    # for row in seating:
    #     print("".join([chr(entry) for entry in row]))
    # print()
    if changes == 0:
        break

print(f"{np.count_nonzero(seating == OCCUPIED)} seats are occupied")


print(".oO( done )")
