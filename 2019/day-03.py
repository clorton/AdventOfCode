#!/usr/bin/env python3

import numpy as np
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


def main(filename):

    with open(filename, 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]

    # lines = [
    #     "R8,U5,L5,D3",
    #     "U7,R6,D4,L4"
    # ]

    # lines = [
    #     "R75,D30,R83,U83,L12,D49,R71,U7,L72",
    #     "U62,R66,U55,R34,D71,R55,D58,R83"
    # ]

    # lines = [
    #     "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
    #     "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
    # ]

    line1 = lines[0].split(',')
    line2 = lines[1].split(',')

    compass = {
        'R': (1, 0),
        'D': (0, 1),
        'L': (-1, 0),
        'U': (0, -1)
    }

    # part 1

    def get_extents(line):

        x = 0
        y = 0
        min_x = 1 << 31
        min_y = 1 << 31
        max_x = -min_x
        max_y = -min_y
        for entry in line:
            direction = entry[0]
            distance = int(entry[1:])
            x += compass[direction][0] * distance
            y += compass[direction][1] * distance
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        return (min_x, min_y, max_x, max_y)

    min_x1, min_y1, max_x1, max_y1 = get_extents(line1)
    min_x2, min_y2, max_x2, max_y2 = get_extents(line2)

    min_x = min(min_x1, min_x2)
    min_y = min(min_y1, min_y2)
    max_x = max(max_x1, max_x2)
    max_y = max(max_y1, max_y2)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    board = np.zeros((height, width), dtype=np.uint32)
    visits = np.zeros_like(board)
    crossings = set()

    x0 = min_x
    y0 = min_y

    def trace_wire(line, marker):

        nonlocal visits, x0, y0, board, crossings
        x = 0
        y = 0
        count = 0
        for entry in line:
            direction = entry[0]
            distance = int(entry[1:])
            for _ in range(distance):
                x += compass[direction][0]
                y += compass[direction][1]
                count += 1
                if (visits[y - y0, x - x0] & marker) == 0:
                    board[y - y0, x - x0] += count
                    visits[y - y0, x - x0] |= marker
                    if visits[y - y0, x - x0] == 3:
                        crossings.add(Point(x, y))

        return

    trace_wire(line1, 1)
    trace_wire(line2, 2)

    minimum = 1 << 31
    for entry in crossings:
        distance = abs(entry.x) + abs(entry.y)
        if distance > 0:
            minimum = min(minimum, distance)

    print(f"Minimum distance is {minimum}.")

    # part 2

    minimum = 1 << 31
    for entry in crossings:
        steps = board[entry.y-y0, entry.x-x0]
        if steps > 0:
            minimum = min(minimum, steps)

    print(f"Minimum steps is {minimum}.")

    return


if __name__ == '__main__':
    main('day-03.txt')
