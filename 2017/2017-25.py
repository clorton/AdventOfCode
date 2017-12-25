#!/usr/bin/python

import numpy


def main():

    turing = {
        'A': [(1, +1, 'B'), (0, -1, 'D')],
        'B': [(1, +1, 'C'), (0, +1, 'F')],
        'C': [(1, -1, 'C'), (1, -1, 'A')],
        'D': [(0, -1, 'E'), (1, +1, 'A')],
        'E': [(1, -1, 'A'), (0, +1, 'B')],
        'F': [(0, +1, 'C'), (0, +1, 'E')]
    }

    state = 'A'
    size = 1000000
    tape = numpy.zeros(size, dtype=numpy.int8)
    position = 0
    for i in range(12317297):
        action = turing[state][tape[position]]
        tape[position] = action[0]
        position += action[1]
        position %= size
        state = action[2]

    print('Checksum is {0}'.format(tape.sum()))

    return


if __name__ == '__main__':
    main()
