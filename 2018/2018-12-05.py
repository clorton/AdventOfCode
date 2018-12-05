#!/usr/bin/python

from __future__ import print_function


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-05.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


def part1(lines):

    polymer = process_polymer(lines[0])

    print('Polymer is {0}'.format(''.join(polymer)))
    print('Polymer length is {0}'.format(len(polymer)))

    return


def process_polymer(string):

    polymer = [c for c in string]
    index = 0
    while index < (len(polymer)-1):
        if abs(ord(polymer[index])-ord(polymer[index+1])) == 32:
            polymer.pop(index)
            polymer.pop(index)
            index = max(index - 1, 0)
        else:
            index += 1

    return polymer


def part2(lines):

    start = lines[0]
    target = None
    minimum = len(lines[0])
    for o in range(ord('A'), ord('Z')+1):
        polymer = process_polymer(start.replace(chr(o), '').replace(chr(o+32), ''))
        if len(polymer) < minimum:
            target = chr(o)
            minimum = len(polymer)

    print("Minimum polymer is {0} units after removing '{1}'.".format(minimum, target))

    return


if __name__ == '__main__':
    main()
