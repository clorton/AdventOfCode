#!/usr/bin/env python3

from collections import namedtuple
from intcode import Computer


Point = namedtuple("Point", ["x", "y"])
BLACK = 0
WHITE = 1
LEFT = 0
RIGHT = 1


def main():

    with open('day-11.txt', 'r') as file:
        inputs = file.read()

    program = [int(entry) for entry in inputs.split(',')]

    directions = [
        Point(0, -1),
        Point(1, 0),
        Point(0, 1),
        Point(-1, 0)
    ]

    robot_x = 0
    robot_y = 0
    direction = 0
    computer = Computer(program, [])
    hull = {}
    painted = set()
    while True:
        location = Point(robot_x, robot_y)
        color = WHITE if location in hull and hull[location] == WHITE else BLACK
        paint = computer.run([color])
        if paint is None:
            break
        turn = computer.run()
        if turn is None:
            break
        hull[location] = paint
        painted.add(location)
        if turn == LEFT:
            direction -= 1
        else:   # turn == RIGHT
            direction += 1
        direction %= len(directions)
        robot_x += directions[direction].x
        robot_y += directions[direction].y

    print(f"# of panels painted = {len(painted)}")

    # Part 2
    robot_x = 0
    robot_y = 0
    direction = 0
    computer = Computer(program, [])
    hull = {Point(robot_x, robot_y): WHITE}
    painted = set()
    while True:
        location = Point(robot_x, robot_y)
        color = WHITE if location in hull and hull[location] == WHITE else BLACK
        paint = computer.run([color])
        if paint is None:
            break
        turn = computer.run()
        if turn is None:
            break
        hull[location] = paint
        painted.add(location)
        if turn == LEFT:
            direction -= 1
        else:   # turn == RIGHT
            direction += 1
        direction %= len(directions)
        robot_x += directions[direction].x
        robot_y += directions[direction].y

    min_x = 1 << 31
    max_x = -min_x
    min_y = min_x
    max_y = max_x
    for point in painted:
        min_x = min(min_x, point.x)
        max_x = max(max_x, point.x)
        min_y = min(min_y, point.y)
        max_y = max(max_y, point.y)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    pixels = [[' ' for _ in range(width)] for __ in range(height)]
    for point in hull:
        if hull[point] == WHITE:
            pixels[point.y-min_y][point.x-min_x] = "#"

    for y in range(height):
        print(''.join(pixels[y]))

    return


if __name__ == "__main__":
    main()
