#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict


def main():

    lines = load_data()
    part1(lines)

    return


def load_data(filename='2018-12-04.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


def part1(lines):

    log = defaultdict(lambda: [0 for _ in range(60)])

    lines.sort()
    guard = None
    sleep = None
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
            raise RuntimeError('Unknown entry: {0}'.format(line))

    max_minutes = 0
    max_id = -1
    for guard in log:
        schedule = log[guard]
        count = 0
        total = 0
        for minute in schedule:
            total += minute
            if minute > 0:
                count += 1
        print('{0} for {1} minutes'.format(guard, total))
        if total > max_minutes:
            max_minutes = total
            max_id = guard

    schedule = log[max_id]
    print('{0}: {1}'.format(max_id, schedule))
    max_index = schedule.index(max(schedule))
    print('Guard {0} slept a total of {1} minutes. Most often on minute {2}.'.format(max_id, max_minutes, max_index))
    print('(guard id) {0} * {1} (index) = {2}'.format(max_id, max_index, max_id*max_index))

    # part 2

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
    print('Guard {0} was asleep on minute {1} {2} times.'.format(max_id, max_index, maximum))
    print('(guard id) {0} * {1} (index) = {2}'.format(max_id, max_index, max_id*max_index))

    return


if __name__ == '__main__':
    main()
