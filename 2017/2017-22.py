#!/usr/bin/python

from enum import IntEnum


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    COUNT = 4


DELTAS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]


def main():

    with open('2017-22.txt', 'r') as handle:
        data = handle.readlines()

    memory = initialize_memory(data)

    infections = process_one(memory)
    print('During 10,000 bursts of activity, virus infected {0} nodes.'.format(infections))

    memory = initialize_memory(data)

    infections = process_two(memory)
    print('After 10,000,000 bursts of activity, evolved virus infected {0} nodes.'.format(infections))

    return


def initialize_memory(data):

    memory = [['.' for _ in range(1001)] for _ in range(1001)]

    for y in range(len(data)):
        row = data[y]
        for x in range(len(row)):
            if row[x] == '#':
                memory[500 - (len(data) // 2) + y][500 - (len(row) // 2) + x] = '#'

    return memory


def process_one(memory, count=10000):

    x_pos = 499
    y_pos = 500
    direction = Direction.UP
    infections = 0
    for i in range(count):

        if memory[y_pos][x_pos] == '#':     # infected
            direction = (direction + 1) % Direction.COUNT
            new = '.'
        elif memory[y_pos][x_pos] == '.':   # clean
            direction = (direction - 1) % Direction.COUNT
            new = '#'
            infections += 1
        else:
            raise RuntimeError('Unexpected node state: {0}'.format(memory[y_pos][x_pos]))

        memory[y_pos][x_pos] = new
        dx, dy = DELTAS[direction]
        x_pos += dx
        y_pos += dy

    return infections


def process_two(memory, count=10000000):

    x_pos = 499
    y_pos = 500
    direction = Direction.UP
    infections = 0
    for i in range(count):

        if memory[y_pos][x_pos] == '#':     # infected -> flagged
            direction = (direction + 1) % Direction.COUNT
            new = 'F'
        elif memory[y_pos][x_pos] == '.':   # clean -> weakened
            direction = (direction - 1) % Direction.COUNT
            new = 'W'
        elif memory[y_pos][x_pos] == 'F':   # flagged -> clean
            direction = (direction + 2) % Direction.COUNT
            new = '.'
        elif memory[y_pos][x_pos] == 'W':   # weakened -> infected
            new = '#'
            infections += 1
        else:
            raise RuntimeError('Unexpected node state: {0}'.format(memory[y_pos][x_pos]))

        memory[y_pos][x_pos] = new
        dx, dy = DELTAS[direction]
        x_pos += dx
        y_pos += dy

    return infections


if __name__ == '__main__':
    main()
