#!/usr/bin/python

from __future__ import print_function


def main():

    lines = load_data()
    offsets = [int(line) for line in lines]
    part1(offsets)
    part2(offsets)

    return


def part1(offsets):

    frequency = 0
    for offset in offsets:
        frequency += offset

    print(frequency)

    return


def part2(offsets):

    frequencies = set()
    frequency = 0
    while True:
        for offset in offsets:
            frequency += offset
            if frequency not in frequencies:
                frequencies.add(frequency)
            else:
                print(frequency)
                return

    return


def load_data(filename='2018-12-01.txt'):

    with open(filename, 'r') as handle:
        data = handle.readlines()
        # data = [line.split() for line in handle.readlines()]

    return data


if __name__ == '__main__':
    main()
