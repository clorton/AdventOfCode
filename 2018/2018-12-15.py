#!/usr/bin/python

from __future__ import print_function


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-15.txt'):

    with open(filename, 'r') as handle:
        data = [line.rstrip() for line in handle.readlines()]

    return data


def part1(lines):

    return


def part2(lines):

    return


if __name__ == '__main__':
    main()
