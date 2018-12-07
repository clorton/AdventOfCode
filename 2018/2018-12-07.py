#!/usr/bin/python

from __future__ import print_function


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-07.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


def part1(lines):

    data = [(line.split()[1], line.split()[7]) for line in lines]

    graph = {}

    for a, b in data:
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[b].add(a)

    steps = []
    while len(graph) > 0:
        available = set()
        for key in graph:
            if len(graph[key]) == 0:
                available.add(key)

        next_steps = [item for item in available]
        next_steps.sort()
        next_step = next_steps[0]

        steps.append(next_step)
        graph.pop(next_step)

        for key in graph:
            if next_step in graph[key]:
                graph[key].remove(next_step)

    print('Step order: {0}'.format(''.join(steps)))

    return


def part2(lines):

    data = [(line.split()[1], line.split()[7]) for line in lines]

    graph = {}

    for a, b in data:
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[b].add(a)

    time = 0
    active = {}
    while len(graph) > 0:
        available = set()
        for key in graph:
            if len(graph[key]) == 0:
                available.add(key)

        available = [item for item in available]
        available.sort()

        while (len(available) > 0) and (len(active) < 5):
            graph.pop(available[0])
            active[available[0]] = ord(available[0]) - 4
            available.pop(0)

        remove = set()
        ready = False
        while not ready:
            time += 1
            for job in active:
                active[job] -= 1
                if active[job] == 0:
                    remove.add(job)
                    ready = True

        for job in remove:
            active.pop(job)
            for key in graph:
                if job in graph[key]:
                    graph[key].remove(job)

    print('Total time: {0}'.format(time))

    return


if __name__ == '__main__':
    main()
