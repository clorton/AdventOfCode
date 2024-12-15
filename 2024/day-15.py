from pathlib import Path
# import re

import numpy as np

with (Path(__file__).parent / "day-15.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

verbose = False

# lines = [
#     "##########",
#     "#..O..O.O#",
#     "#......O.#",
#     "#.OO..O.O#",
#     "#..O@..O.#",
#     "#O#..O...#",
#     "#O..O..O.#",
#     "#.OO.O.OO#",
#     "#....O...#",
#     "##########",
#     "",
#     "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^",
#     "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v",
#     "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<",
#     "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^",
#     "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><",
#     "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^",
#     ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^",
#     "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>",
#     "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>",
#     "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^",
# ]

# verbose = True

# lines = [
#     "########",
#     "#..O.O.#",
#     "##@.O..#",
#     "#...O..#",
#     "#.#.O..#",
#     "#...O..#",
#     "#......#",
#     "########",
#     "",
#     "<^^>>>vv<v>>v<<",
# ]

# verbose = True

WALL = ord("#")
SPACE = ord(".")
ROBOT = ord("@")
BOX = ord("O")

floormap = []
moves = ""
empty = False
for line in lines:
    if line == "":
        empty = True
        continue
    if not empty:
        floormap.append(line)
    else:
        moves += line

floormap = np.array([list(map(ord, list(row))) for row in floormap], dtype=np.int8)
save = np.array(floormap, dtype=np.int8)

ry, rx = np.where(floormap == ROBOT)
rx, ry = rx[0], ry[0]


def trymove(rx, ry, dx, dy, floormap, verbose=False):

    if verbose:
        print(f"Trying to move {dx}, {dy} from {rx}, {ry}...")

    moves = 0
    tx, ty = rx, ry
    while True:
        tx, ty = tx + dx, ty + dy
        if floormap[ty, tx] == WALL:
            if verbose:
                print("Hit a wall.")
            return rx, ry
        moves += 1
        if floormap[ty, tx] == BOX:
            continue
        if floormap[ty, tx] == SPACE:
            break
    if verbose:
        print(f"Moving {moves} steps.")
    for i in range(moves):
        floormap[ty, tx] = floormap[ty-dy, tx-dx]
        tx, ty = tx - dx, ty - dy
    floormap[ry, rx] = SPACE

    if verbose:
        for row in floormap:
            print("".join(map(chr, row)))
        print("\n")

    return rx+dx, ry+dy

for move in list(moves):
    if move == "<":
        rx, ry = trymove(rx, ry, -1, 0, floormap)
    elif move == ">":
        rx, ry = trymove(rx, ry, +1, 0, floormap)
    elif move == "^":
        rx, ry = trymove(rx, ry, 0, -1, floormap)
    elif move == "v":
        rx, ry = trymove(rx, ry, 0, +1, floormap)

    # floormap[rx, ry] = ROBOT

for row in floormap:
    print("".join(map(chr, row)))
print("\n")

def gps(floormap):
    total = 0
    ys, xs = np.where(floormap == BOX)
    for x, y in zip(xs, ys):
        total += 100 * y + x
    return total

print(gps(floormap))

LBOX = ord("[")
RBOX = ord("]")

widen = {
    WALL: [WALL, WALL],
    SPACE: [SPACE, SPACE],
    ROBOT: [ROBOT, SPACE],
    BOX: [LBOX, RBOX],
}

print("\n----------==========########## Widening... ##########==========----------\n")

height, width = save.shape
floormap2 = np.zeros((height, width*2), dtype=np.int8)
for y, row in enumerate(save):
    for x, value in enumerate(row):
        floormap2[y, 2*x:2*x+2] = widen[value]

for row in floormap2:
    print("".join(map(chr, row)))
print("\n")

def trymove2(rx, ry, dx, dy, floormap, verbose=False):

    if verbose:
        print(f"Trying to move {dx}, {dy} from {rx}, {ry}...")

    rows = [{(rx, ry)}]
    while rows[-1]:
        row = rows[-1]
        nextrow = set()
        for tx, ty in row:
            tx, ty = tx + dx, ty + dy
            if floormap[ty, tx] == WALL:
                if verbose:
                    print("Hit a wall.")
                return rx, ry
            if floormap[ty, tx] == LBOX:
                nextrow.update({(tx, ty), (tx+1, ty)})
                continue
            if floormap[ty, tx] == RBOX:
                nextrow.update({(tx-1, ty), (tx, ty)})
                continue
        rows.append(nextrow)
    while rows:
        row = rows.pop()
        for tx, ty in row:
            floormap[ty+dy, tx+dx] = floormap[ty, tx]
            floormap[ty, tx] = SPACE

    if verbose:
        for row in floormap:
            print("".join(map(chr, row)))
        print("\n")

    return rx+dx, ry+dy

ry, rx = np.where(floormap2 == ROBOT)
rx, ry = rx[0], ry[0]

for move in list(moves):
    if move == "<":
        rx, ry = trymove(rx, ry, -1, 0, floormap2, verbose=verbose)
    elif move == ">":
        rx, ry = trymove(rx, ry, +1, 0, floormap2, verbose=verbose)
    elif move == "^":
        rx, ry = trymove2(rx, ry, 0, -1, floormap2, verbose=verbose)
    elif move == "v":
        rx, ry = trymove2(rx, ry, 0, +1, floormap2, verbose=verbose)

for row in floormap2:
    print("".join(map(chr, row)))
print("\n")

def gps2(floormap):
    total = 0
    ys, xs = np.where(floormap == LBOX)
    for x, y in zip(xs, ys):
        total += 100 * y + x
    return total

print(gps2(floormap2))


print("Done.")
