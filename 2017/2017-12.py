#!/usr/bin/python

from collections import defaultdict, deque


def get_input(filename='2017-12.txt'):
    with open(filename, 'r') as handle:
        data = handle.readlines()

    return data


def main():

    data = get_input()
    map = defaultdict(set)
    for line in data:
        program, neighbors = [item.strip() for item in line.split('<->')]
        neighbors = [neighbor.strip() for neighbor in neighbors.split(',')]
        for neighbor in neighbors:
            map[program].add(neighbor)
            map[neighbor].add(program)

    visited = set()
    next = deque()
    next.append('0')
    while len(next) > 0:
        current = next.popleft()
        if current not in visited:
            visited.add(current)
            next.extend(map[current])

    print('Size of group 0 is {0}'.format(len(visited)))

    groups = 0
    while len(map) > 0:
        visited = set()
        next = deque()
        key = [key for key in map.keys()][0]
        next.append(key)
        while len(next) > 0:
            current = next.popleft()
            if current not in visited:
                visited.add(current)
                next.extend(map.pop(current))
        groups += 1

    print('Found {0} groups'.format(groups))

    return


if __name__ == '__main__':
    main()
