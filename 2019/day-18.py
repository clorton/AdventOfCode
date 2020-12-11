#!/usr/bin/env python3

from collections import namedtuple

Point = namedtuple("Point", ["row", "col"])
Delta = namedtuple("Delta", ["dx", "dy"])
Key = namedtuple("Item", ["name", "point", "distance"])

ENTRANCE = "@"
PASSAGE = "."
WALL = "#"
KEYS = "abcdefghijklmnopqrstuvwxyz"
DOORS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DELTAS = [
    Delta(0, -1),   # North
    Delta(0, 1),    # South
    Delta(1, 0),    # East
    Delta(-1, 0)    # West
]


def get_keys(tunnels, start):
    initial = set()
    initial.add(start)
    fill = [initial]
    tested = set()
    tested.add(start)
    keys = []
    doors = {}
    while len(fill[-1]) > 0:
        subsequent = set()
        for point in fill[-1]:
            tested.add(point)
            distance = len(fill)
            for adjacent in range(4):
                test = Point(point.row + DELTAS[adjacent].dy, point.col + DELTAS[adjacent].dx)
                cell = tunnels[test.row][test.col]
                if cell == WALL:
                    continue
                elif cell == PASSAGE or cell == ENTRANCE:
                    if test not in tested:
                        subsequent.add(test)
                elif cell in KEYS:
                    # print(f"Found key  '{cell}' at {test} {distance} steps away.")
                    keys.append(Key(cell, test, distance))
                elif cell in DOORS:
                    # print(f"Found door '{cell}' at {test}")
                    doors[cell] = test
                else:
                    raise RuntimeError(f"Unknown cell type {tunnels[test.row][test.col]}")

        fill.append(subsequent)

    return sorted(keys, key=lambda k: k.distance), doors


def find_path(start, tunnels, doors):

    steps = 1 << 31
    path = [start]

    tunnels[start.point.row][start.point.col] = PASSAGE
    keys, _ = get_keys(tunnels, start.point)
    # print(f"Found {len(keys)} keys and {len(_)} doors.")
    if len(keys) > 0:
        for key in keys:
            door = doors[key.name.upper()]
            tunnels[door.row][door.col] = PASSAGE
            distance, best = find_path(key, tunnels, doors)
            if distance < steps:
                steps = distance
                path = [key]
                path.extend(best)

            tunnels[door.row][door.col] = key.name.upper()
    else:
        steps = 0

    tunnels[start.point.row][start.point.col] = start.name

    return steps, path


def main():

    with open('day-18.txt', "r") as file:
        tunnels = [[c for c in line.strip()] for line in file.readlines()]

    entrance = None
    doors = {}
    for row in range(len(tunnels)):
        for col in range(len(tunnels[row])):
            if tunnels[row][col] in DOORS:
                doors[tunnels[row][col]] = Point(row, col)
            elif tunnels[row][col] == ENTRANCE:
                entrance = Point(row, col)

    start = Key("@", entrance, 0)
    total, path = find_path(start, tunnels, doors)

    print(f"Total steps: {total}.")
    print(f"Path: {path}")
    # 4250 :(

    return


if __name__ == "__main__":
    main()
