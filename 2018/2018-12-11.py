#!/usr/bin/python

from __future__ import print_function


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-11.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


def part1(lines):

    serial = 1133
    grid = [[None for _ in range(301)] for __ in range(301)]
    for y in range(1, 301):
        for x in range(1, 301):
            rackId = x + 10
            power = rackId * y
            power += serial
            power *= rackId
            power /= 100
            power %= 10
            power -= 5
            grid[y][x] = power

    max_power = 0
    location = (1, 1)
    for y in range(1, 299):
        for x in range(1, 299):
            power = 0
            for j in range(3):
                for i in range(3):
                    power += grid[y+j][x+i]
            if power > max_power:
                max_power = power
                location = (x, y)

    print('Max power {0} at {1}'.format(max_power, location))

    return


def part2(lines):

    serial = 1133
    grid = [[0 for _ in range(301)] for __ in range(301)]
    for y in range(1, 301):
        for x in range(1, 301):
            rackId = x + 10
            power = rackId * y
            power += serial
            power *= rackId
            power /= 100
            power = int(power)
            power %= 10
            power -= 5
            grid[y][x] = power

    sumx = [[0 for _ in range(301)] for __ in range(301)]
    for y in range(1, 301):
        for x in range(1, 301):
            sumx[y][x] = grid[y][x] + sumx[y][x-1]

    sumy = [[0 for _ in range(301)] for __ in range(301)]
    for x in range(1, 301):
        for y in range(1, 301):
            sumy[y][x] = sumx[y][x] + sumy[y-1][x]

    max_power = 0
    location = (1, 1, 1)
    for size in range(1, 301):
        print('Considering {0}...'.format(size))
        for y in range(1, 301-size):
            for x in range(1, 301-size):
                power = sumy[y+size-1][x+size-1]
                power -= sumy[y+size-1][x-1]
                power -= sumy[y-1][x+size-1]
                power += sumy[y-1][x-1]
                if power > max_power:
                    max_power = power
                    location = (x, y, size)
                    print('Max power so far is {0} at {1}'.format(max_power, location))

    print('Max power {0} at {1}'.format(max_power, location))

    return


if __name__ == '__main__':
    main()
