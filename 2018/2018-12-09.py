#!/usr/bin/python

from __future__ import print_function
import numpy


def main():

    lines = None    # load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-09.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


NUM_PLAYERS = 476
MAX_MARBLE = 71657


def part1(lines):

    circle = [0, 1]
    current = 1
    scores = [0 for _ in range(NUM_PLAYERS)]
    for marble in range(2, MAX_MARBLE+1):
        if (marble % 23) != 0:
            if current < (len(circle) - 2):
                position = current + 2
                circle.insert(position, marble)
            elif current == (len(circle) - 2):
                position = len(circle)
                circle.append(marble)
            elif current == (len(circle) - 1):
                position = 1
                circle.insert(position, marble);
            current = position
        else:
            player = marble % NUM_PLAYERS
            scores[player] += marble
            seven_cc = (current - 7) % len(circle)
            scores[player] += circle[seven_cc]
            circle.pop(seven_cc)
            current = seven_cc

    print('Scores: {0}'.format(scores))
    print('Max score is {0}'.format(max(scores)))

    return


VALU = 0
NEXT = 1
PREV = 2


def part2(lines):
    """ Lists are too slow for x100 challenge, use a double linked list implemented in an array. """

    circle = numpy.zeros((MAX_MARBLE*100, 3), numpy.uint32)
    newest = 1
    current = 0
    scores = [0 for _ in range(NUM_PLAYERS)]
    for marble in range(1, MAX_MARBLE*100):
        if (marble % 23) != 0:
            clockwise = circle[current, NEXT]
            circle[newest, VALU] = marble
            circle[newest, NEXT] = circle[clockwise, NEXT]
            circle[newest, PREV] = clockwise
            circle[clockwise, NEXT] = newest
            circle[circle[newest, NEXT], PREV] = newest
            current = newest
            newest += 1
#            if marble <= 25:
#                print_circle(circle, current)
        else:
            player = marble % NUM_PLAYERS
            scores[player] += marble
            for _ in range(7):
                current = circle[current, PREV]
            scores[player] += circle[current, VALU]
            circle[circle[current, PREV], NEXT] = circle[current, NEXT]
            circle[circle[current, NEXT], PREV] = circle[current, PREV]
            current = circle[current, NEXT]
#            if marble <= 25:
#                print_circle(circle, current)

    print('Scores: {0}'.format(scores))
    print('Max score is {0}'.format(max(scores)))

    return


def print_circle(circle, current):

    index = 0
    while True:
        if index != current:
            print('{0} '.format(circle[index, VALU]), end='')
        else:
            print('({0}) '.format(circle[index, VALU]), end='')
        index = circle[index, NEXT]
        if index == 0:
            break
    print()

    return


if __name__ == '__main__':
    main()
