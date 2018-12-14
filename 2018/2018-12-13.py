#!/usr/bin/python

from __future__ import print_function
import functools
import time


def main():

    lines = load_data()
    part2(lines)

    return


def load_data(filename='2018-12-13.txt'):

    with open(filename, 'r') as handle:
        data = [line.rstrip() for line in handle.readlines()]

    return data


LEFT = 0
STRAIGHT = 1
RIGHT = 2

X = 0
Y = 1
V = 2
TURN = 3
DIRECTION = 4

DX = 0
DY = 1

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

VECTORS = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0)
}


def part2(lines):

    track, carts = load_track(lines)

    tick = 0
    while True:
        tick += 1
        carts.sort(key=functools.cmp_to_key(cart_comparator))
        remove = set()
        for i in range(len(carts)):
            if i in remove:
                continue

            cart = carts[i]

            cart[X] += cart[V][DX]
            cart[Y] += cart[V][DY]

            x = cart[X]
            y = cart[Y]
            for j in range(len(carts)):
                if j != i:
                    if (carts[j][X] == x) and (carts[j][Y] == y):
                        print('On tick {4} remove carts {0} and {1} at ({2}, {3})'.format(i, j, x, y, tick))
                        remove.add(i)
                        remove.add(j)

            cell = track[y][x]

            if cell == '/':
                if (cart[DIRECTION] == NORTH) or (cart[DIRECTION] == SOUTH):
                    turn_right(cart)
                elif (cart[DIRECTION] == EAST) or (cart[DIRECTION] == WEST):
                    turn_left(cart)
                else:
                    raise RuntimeError('??')
            elif cell == '\\':
                if (cart[DIRECTION] == NORTH) or (cart[DIRECTION] == SOUTH):
                    turn_left(cart)
                elif (cart[DIRECTION] == EAST) or (cart[DIRECTION] == WEST):
                    turn_right(cart)
                else:
                    raise RuntimeError('???')
            elif cell == '+':
                if cart[TURN] == LEFT:
                    turn_left(cart)
                elif cart[TURN] == STRAIGHT:
                    pass
                elif cart[TURN] == RIGHT:
                    turn_right(cart)

                cart[TURN] += 1
                cart[TURN] %= 3

        # display(tick, track, carts)

        if len(remove) > 0:
            remove = [i for i in remove]
            remove.sort(reverse=True)
            for i in remove:
                carts.pop(i)

        if len(carts) == 1:
            # display(tick, track, carts)
            print('Last cart {0}'.format(carts[0]))
            break

    return


def turn_left(cart):

    cart[DIRECTION] -= 1
    cart[DIRECTION] %= 4
    cart[V] = VECTORS[cart[DIRECTION]]

    return


def turn_right(cart):

    cart[DIRECTION] += 1
    cart[DIRECTION] %= 4
    cart[V] = VECTORS[cart[DIRECTION]]

    return

def load_track(lines):

    track = [[c for c in line] for line in lines]
    #    data = [ '/->-\\', '|   |  /----\\', '| /-+--+-\\  |', '| | |  | v  |', '\\-+-/  \\-+--/', '  \\------/']
    #    track = [[c for c in line] for line in data]
    carts = []
    for y in range(len(track)):
        row = track[y]
        for x in range(len(row)):
            cell = row[x]
            if cell == '^':
                row[x] = '|'
                carts.append([x, y, (0, -1), LEFT, NORTH])
            elif cell == 'v':
                row[x] = '|'
                carts.append([x, y, (0, 1), LEFT, SOUTH])
            elif cell == '<':
                row[x] = '-'
                carts.append([x, y, (-1, 0), LEFT, WEST])
            elif cell == '>':
                row[x] = '-'
                carts.append([x, y, (1, 0), LEFT, EAST])

    return track, carts


def cart_comparator(a, b):
    if a[Y] < b[Y]:
        return -1
    if a[Y] > b[Y]:
        return 1
    if a[X] < b[X]:
        return -1
    if a[X] > b[X]:
        return 1

    print('Collision at ({0}, {1})'.format(a[X], a[Y]))
    raise RuntimeError('?')


def display(tick, track, carts):

    print('After tick {0}'.format(tick))
    output = [[c for c in row] for row in track]
    for cart in carts:
        try:
            output[cart[Y]][cart[X]] = '*'
        except:
            raise RuntimeError('????')
    y = 1
    for row in output:
        print(''.join(row))
        y += 1
    print()

    return


if __name__ == '__main__':
    main()
