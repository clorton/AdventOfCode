#!/usr/bin/python


from enum import IntEnum


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    COUNT = 4


def main():

    with open('2017-19.txt', 'r') as handle:
        data = [line.rstrip() for line in handle.readlines()]

    lengths = [length for length in map(len, data)]
    length = max(lengths) + 1
    spaces = [' ' for i in range(length)]
    pad = ''.join(spaces)

    data = [line + pad[len(line):] for line in data]

    deltas = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0)
    ]

    x = data[0].index('|')
    y = 0
    direction = Direction.DOWN
    visited = []
    count = 0

    while True:
        count += 1
        pipe = data[y][x]
        if pipe in '|-':
            dx, dy = deltas[direction]
            x += dx
            y += dy
        elif pipe.isalpha():
            visited.append(pipe)
            dx, dy = deltas[direction]
            x += dx
            y += dy
        elif pipe == '+':
            for i in range(Direction.COUNT):
                test = (direction - 1 + i) % Direction.COUNT
                dx, dy = deltas[test]
                if data[y+dy][x+dx] in '|-':
                    x += dx
                    y += dy
                    direction = test
                    break
        else:
            count -= 1
            break

    print('Visited {0} after {1} steps'.format(''.join(visited), count))

    return


if __name__ == '__main__':
    main()
