#!/usr/bin/python

from __future__ import print_function
from collections import namedtuple
import re


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-10.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


Point = namedtuple('Point', ['x', 'y', 'dx', 'dy'])


def part1(lines):

    pattern = re.compile('position=<(.{6}), (.{6})> velocity=<(.{2}), (.{2})>')
    points = []
    for line in lines:
        m = pattern.match(line)
        points.append(Point(*[int(element.strip()) for element in m.groups()]))

    for t in range(10105, 10106):
        data = []
        for p in points:
            data.append(Point(p.x + p.dx*t, p.y + p.dy*t, 0, 0))
        xs = [p.x for p in data]
        ys = [p.y for p in data]
        min_x = min(xs)
        min_y = min(ys)
        max_x = max(xs)
        max_y = max(ys)
        print('{6}: ({0},{1}) - ({2},{3}) [{4}x{5}]'.format(min_x, min_y, max_x, max_y, max_x - min_x, max_y - min_y, t))
        canvas = [[' ' for _ in range(min_x, max_x+1)] for __ in range(min_y, max_y+1)]
        for p in data:
            canvas[p.y-min_y][p.x-min_x] = '*'
        for row in canvas:
            print(''.join(row))
        print('\n\n\n')

    return


def part2(lines):

    return


if __name__ == '__main__':
    main()
