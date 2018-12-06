#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])
Entry = namedtuple('Entry', ['point', 'distance'])


def main():

    data = load_data()
    part1(data)
    part2(data)

    return


def load_data(filename='2018-12-06.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    data = [Point(int(entry.split(', ')[0]), int(entry.split(', ')[1])) for entry in data]

    return data


def part1(data):

    xs = [p.x for p in data]
    # min_x = min(xs)
    max_x = max(xs)

    ys = [p.y for p in data]
    # min_y = min(ys)
    max_y = max(ys)

    left = 0
    right = max_x + 40
    top = 0
    bottom = max_y + 40

    plane = [[Entry(None, 1000000) for _ in range(right + 1)] for __ in range(bottom + 1)]

    # Mark each cell in the plane with the index of the nearest point or None if two points are equidistant.
    for i in range(len(data)):
        point = data[i]
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                distance = abs(point.x - x) + abs(point.y - y)
                if distance < plane[y][x].distance:
                    plane[y][x] = Entry(i, distance)
                elif distance == plane[y][x].distance:
                    plane[y][x] = Entry(None, distance)

    # Find the area of each region nearest each point.
    areas = defaultdict(lambda: 0)
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if plane[y][x].point:
                areas[plane[y][x].point] += 1

    # remove the points associated with the areas extending to the border

    points = set([i for i in range(len(data))])
    remove = set()

    for x in range(left, right + 1):
        remove.add(plane[0][x].point)
        remove.add(plane[max_y+40][x].point)

    for y in range(top, bottom + 1):
        remove.add(plane[y][0].point)
        remove.add(plane[y][max_x+40].point)

    points -= remove

    # determine the maximum area of nearest cells for the remaining points
    maximum = 0
    for point in points:
        if areas[point] > maximum:
            maximum = areas[point]

    print('Maximum area is {0}'.format(maximum))

    return


def part2(data):

    xs = [p.x for p in data]
    min_x = min(xs)
    max_x = max(xs)

    ys = [p.y for p in data]
    min_y = min(ys)
    max_y = max(ys)

    left = 0
    right = max_x + 40
    top = 0
    bottom = max_y + 40

    # for each cell in the plane, sum the distance to each of the points

    plane = [[0 for _ in range(right + 1)] for __ in range(bottom + 1)]

    for point in data:
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                distance = abs(point.x - x) + abs(point.y - y)
                plane[y][x] += distance

    # count the number of cells whose distance sum is less than 10000

    total = 0
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if plane[y][x] < 10000:
                total += 1

    print('Total = {0}'.format(total))

    return


if __name__ == '__main__':
    main()
