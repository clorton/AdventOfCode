#!/usr/bin/env python3

from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def main():

    # Part1 AA to ZZ
    with open('day-20.txt', "r") as file:
        maze = [list(line.rstrip()) for line in file.readlines()]

    portals = {}

    y = 0
    for x in range(len(maze[0])):
        if maze[y][x] in UPPER:
            key = maze[y][x] + maze[y+1][x]
            portals[key] = Point(x, y+2) if key not in portals else [portals[key], Point(x, y+2)]

    y = 27
    for x in range(len(maze[27])):
        if maze[y][x] in UPPER:
            key = maze[y][x] + maze[y+1][x]
            portals[key] = Point(x, y-1) if key not in portals else [portals[key], Point(x, y-1)]

    y = 80
    for x in range(len(maze[80])):
        if maze[y][x] in UPPER:
            key = maze[y][x] + maze[y+1][x]
            portals[key] = Point(x, y+2) if key not in portals else [portals[key], Point(x, y+2)]

    y = 107
    for x in range(len(maze[-1])):
        if maze[y][x] in UPPER:
            key = maze[y][x] + maze[y+1][x]
            portals[key] = Point(x, y-1) if key not in portals else [portals[key], Point(x, y-1)]

    x = 0
    for y in range(len(maze)):
        if maze[y][0] in UPPER:
            key = maze[y][0] + maze[y][1]
            portals[key] = Point(2, y) if key not in portals else [portals[key], Point(2, y)]

    x = 27
    for y in range(27, 83):
        if maze[y][x] in UPPER:
            key = maze[y][x] + maze[y][x+1]
            portals[key] = Point(x-1,y ) if key not in portals else [portals[key], Point(x-1, y)]

    x = 78
    for y in range(27, 83):
        if maze[y][x] in UPPER:
            key = maze[y][x] + maze[y][x+1]
            portals[key] = Point(x+2, y) if key not in portals else [portals[key], Point(x+2, y)]

    x = 105
    for y in range(2, len(maze)-2):
        if maze[y][-1] in UPPER:
            key = maze[y][-2] + maze[y][-1]
            portals[key] = Point(x-1, y) if key not in portals else [portals[key], Point(x-1, y)]

    links = {}
    for key, value in portals.items():
        if isinstance(value, list):
            links[value[0]] = (key, value[1])
            links[value[1]] = (key, value[2])
            maze[value[0].y][value[0].x] = maze[value[1].y][value[1].x] = "@"
        elif isinstance(value, type(Point)):
            links[value] = (key, None)
            maze[value.y][value.x] = "@"
        else:
            raise RuntimeError(f"Unknown value in portals dictionary: {value}")

    def find_portals(start, maze, links):

        queue = [list(start)]
        while len(queue[-1]) > 0:
            pass

        return

    start = aa
    ports = find_portals(start, maze, links)

    print(f"From {start} found the following ports: {ports}")

    return


if __name__ == "__main__":
    main()
