#!/usr/bin/python

from functools import reduce

with open('2017-10.txt', 'r') as handle:
    line = handle.readline()


def contents(source, index, count):
    return [source[i % len(source)] for i in range(index, index+count)]


def update(destination, index, count, source):
    for i in range(count):
        destination[(index+i) % len(destination)] = source[i]


lengths = [int(entry) for entry in line.split(',')]
memory = [i for i in range(256)]
current_position = 0
skip_size = 0
for length in lengths:
    extract = contents(memory, current_position, length)
    reverse = [item for item in reversed(extract)]
    update(memory, current_position, length, reverse)
    current_position += length + skip_size
    skip_size += 1

product = memory[0] * memory[1]
print('memory[0] = {0}, memory[1] = {1}, product = {2}'.format(memory[0], memory[1], product))


lengths = [int(b) for b in bytes(line, 'utf-8')]
lengths.extend([17,31,73,47,23])
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

hash = [reduce(lambda x, y: x ^ y, memory[start:start+16]) for start in range(0, 256, 16)]
string = reduce(lambda x, y: x + '{0:02x}'.format(y), hash, '')
print('Hash = {0}'.format(hash))
print('Hex  = {0}'.format(string))
