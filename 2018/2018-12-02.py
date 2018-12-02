#!/usr/bin/python

from __future__ import print_function


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-02.txt'):

    with open(filename, 'r') as handle:
        data = handle.readlines()

    return data


def part1(lines):

    twos = 0
    threes = 0
    for line in lines:
        histogram = [0 for _ in range(26)]
        for letter in line.strip():
            histogram[ord(letter)-ord('a')] += 1
        counts = set()
        for entry in histogram:
            counts.add(entry)

        if 2 in counts:
            twos += 1

        if 3 in counts:
            threes += 1

    print('twos =     {0}'.format(twos))
    print('threes =   {0}'.format(threes))
    print('checksum = {0}'.format(twos * threes))

    return


def part2(lines):

    for ia in range(len(lines)-1):
        source = lines[ia].strip()
        for ib in range(ia, len(lines)):
            compare = lines[ib].strip()
            diffs = 0
            for i in range(len(source)):
                if source[i] != compare[i]:
                    diffs += 1
            if diffs == 1:
                print('{0}'.format(source))
                print('{0}'.format(compare))

    return


if __name__ == '__main__':
    main()
