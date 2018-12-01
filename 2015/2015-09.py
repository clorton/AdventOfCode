#!/usr/bin/python

from collections import defaultdict


def main():

    inputs = get_input('2015-09.txt')
    permutations = get_permutations(8)

    return


def get_input(filename):

    inputs = defaultdict(dict)
    with open(filename, 'r') as handle:
        lines = [line.strip() for line in handle.readlines()]

    for line in lines:
        source, _, destination, _, distance = line.split()
        distance = int(distance)
        inputs[source][destination] = distance
        inputs[destination][source] = distance

    return inputs


def get_permutations(options):

    if len(options) == 0:
        return None

    if len(options) == 1:
        return options




if __name__ == '__main__':
    main()
