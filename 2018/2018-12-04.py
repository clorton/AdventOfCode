#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-04.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


def part1(lines):

    log = defaultdict(lambda: [0 for _ in range(60)])

    lines.sort()
    guard = -1
    for line in lines:
        if 'begins' in line:
            guard = int(line.replace('#', '').split()[3])
        elif 'asleep' in line:
            sleep = int(line[15:17])
        elif 'wakes' in line:
            wake = int(line[15:17])
            for minute in range(sleep, wake):
                log[guard][minute] += 1
        else:
            raise RuntimeError('Unknown entry: {0}'.line)

    max_minutes = 0
    max_id = -1
    for guard in log:
        schedule = log[guard]
        count = 0
        sum = 0
        for minute in schedule:
            sum += minute
            if minute > 0:
                count += 1
        print('{0} for {1} minutes'.format(guard, sum))
        if sum > max_minutes:
            max_minutes = sum
            max_id = guard

    schedule = log[max_id]
    print('{0}: {1}'.format(max_id, schedule))
    max_index = schedule.index(max(schedule))
    print('{0} * (index) {1} = {2}'.format(max_id, max_index, max_id*max_index))

    maximum = 0
    max_id = -1
    for guard in log:
        schedule = log[guard]
        guard_max = max(schedule)
        if guard_max > maximum:
            maximum = guard_max
            max_id = guard

    schedule = log[max_id]
    print('{0}: {1}'.format(max_id, schedule))
    max_index = schedule.index(max(schedule))
    print('{0} * (index) {1} = {2}'.format(max_id, max_index, max_id*max_index))

    return


def part2(lines):

    return


if __name__ == '__main__':
    main()
