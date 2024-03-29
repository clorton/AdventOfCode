#!/usr/bin/env python3

from pathlib import Path

import numpy

WORKDIR = Path(__file__).parent.absolute()

class State(object):
    def __init__(self, size=16):
        self._size = size
        self._where = numpy.array(range(size), dtype=numpy.byte)    # where to find 'a'...'p'
        self._which = numpy.array(range(size), dtype=numpy.byte)    # which character in 0...16
        self._offset = 0

        return

    def spin(self, distance):
        self._where += distance
        self._where %= self._size
        for i in range(self._size):
            self._which[self._where[i]] = i

        return

    def exchange(self, index_a, index_b):
        a, b = self._which[index_a], self._which[index_b]
        self._where[a], self._where[b] = index_b, index_a
        self._which[index_a], self._which[index_b] = b, a

        return

    def partner(self, a, b):
        a = ord(a) - 97 # ord('a')
        b = ord(b) - 97 # ord('a')
        index_a, index_b = self._where[a], self._where[b]
        self._where[a], self._where[b] = index_b, index_a
        self._which[index_a], self._which[index_b] = b, a

        return

    def __str__(self):
        return ''.join([chr(element + ord('a')) for element in self._which])


def main():

    with (WORKDIR / '2017-16.txt').open("r") as handle:
        dance = handle.readline().split(',')

    programs = list('abcdefghijklmnop')
    programs = one_round(programs, dance)
    print('One round final arrangement = {"".join(programs)}\n')

    moves = get_dance_moves(dance)

    state = State()
    cycle = 0
    target = str(state)
    while True:
        cycle += 1
        a_round(state, moves)
        if str(state) == target:
            break

    print(f"cycle = {cycle}")
    ROUNDS = 1_000_000_000 % cycle
    print(f"ROUNDS = {ROUNDS}")

    state = State()
    for i in range(ROUNDS):
        print(f'{i:3}: {state}')
        a_round(state, moves)
    print(f'State final arrangement ({ROUNDS} rounds) = {state}\n')

    return


def one_round(programs, dance):
    for move in dance:
        if move[0] == 's':
            distance = int(move[1:])
            programs = spin(programs, distance)
        elif move[0] == 'x':
            a, b = [int(element) for element in move[1:].split('/')]
            programs = exchange(programs, a, b)
        elif move[0] == 'p':
            a, b = move[1:].split('/')
            programs = partner(programs, a, b)

    return programs


def spin(programs, distance=0):
    length = len(programs)
    result = [programs[(i-distance) % length] for i in range(length)]

    return result


def exchange(programs, a=0, b=0):
    result = [element for element in programs]
    result[a], result[b] = result[b], result[a]

    return result


def partner(programs, a='a', b='a'):
    result = exchange(programs, ''.join(programs).find(a), ''.join(programs).find(b))

    return result


def get_dance_moves(dance):
    moves = []
    for move in dance:
        if move[0] == 's':
            distance = int(move[1:])
            moves.append(('s', distance))
        elif move[0] == 'x':
            a, b = [int(element) for element in move[1:].split('/')]
            moves.append(('x', a, b))
        elif move[0] == 'p':
            a, b = move[1:].split('/')
            moves.append(('p', a, b))

    return moves


def do_spin(state, distance=0):
    state.spin(distance)
    return


def do_exchange(state, a=0, b=0):
    state.exchange(a, b)
    return


def do_partner(state, a='a', b='a'):
    state.partner(a, b)
    return


def a_round(state, moves):
    for move in moves:
        if move[0] == 's':
            state.spin(move[1])
        elif move[0] == 'x':
            state.exchange(move[1], move[2])
        elif move[0] == 'p':
            state.partner(move[1], move[2])

    return


if __name__ == '__main__':
    main()
