#!/usr/bin/python

from collections import deque
from functools import reduce


def main():

    bits = {
        '0': 0,
        '1': 1,
        '2': 1,
        '3': 2,
        '4': 1,
        '5': 2,
        '6': 2,
        '7': 3,
        '8': 1,
        '9': 2,
        'a': 2,
        'b': 3,
        'c': 2,
        'd': 3,
        'e': 3,
        'f': 4
    }

    data = get_input()
    count = 0
    for row in range(128):
        key = '{0}-{1}'.format(data, row)
        _, string = knot_hash(key)
        for nibble in string:
            count += bits[nibble]

    print('Count of 1s is {0}'.format(count))

    memory = [[0 for i in range(128)] for j in range(128)]
    data = get_input()
    for row in range(128):
        key = '{0}-{1}'.format(data, row)
        hash, _ = knot_hash(key)
        column = 0
        for byte in hash:
            mask = 128
            while mask != 0:
                if (byte & mask) != 0:
                    memory[row][column] = 1
                mask >>= 1
                column += 1

    count = 0
    for row in range(128):
        for column in range(128):
            if memory[row][column] != 0:
                count += 1
                clear_region(column, row, memory)

    print('Count of regions is {0}'.format(count))

    return


def get_input(filename='2017-14.txt'):

    return 'amgozmfv'
    # return 'flqrgnkx'


def knot_hash(key):
    lengths = [int(b) for b in bytes(key, 'utf-8')]
    lengths.extend([17, 31, 73, 47, 23])
    memory = [i for i in range(256)]
    current_position = 0
    skip_size = 0
    for round in range(64):
        for length in lengths:
            extract = contents(memory, current_position, length)
            reverse = [item for item in reversed(extract)]
            update(memory, current_position, length, reverse)
            current_position += length + skip_size
            skip_size += 1

    hash = [reduce(lambda x, y: x ^ y, memory[start:start + 16]) for start in range(0, 256, 16)]
    string = reduce(lambda x, y: x + '{0:02x}'.format(y), hash, '')
    # print('Hash = {0}'.format(hash))
    # print('Hex  = {0}'.format(string))

    return hash, string


def contents(source, index, count):
    return [source[i % len(source)] for i in range(index, index+count)]


def update(destination, index, count, source):
    for i in range(count):
        destination[(index+i) % len(destination)] = source[i]

    return


def clear_region(column, row, memory):
    queue = deque()
    queue.append((column, row))
    while len(queue) > 0:
        column, row = queue.popleft()
        if memory[row][column] != 0:
            memory[row][column] = 0
            if row > 0:
                queue.append((column, row-1))
            if row < 127:
                queue.append((column, row+1))
            if column > 0:
                queue.append((column-1, row))
            if column < 127:
                queue.append((column+1, row))

    return


if __name__ == '__main__':
    main()
