#!/usr/bin/python

with open('2017-11.txt', 'r') as handle:
    steps = handle.readline().strip().split(',')

deltas = {
    'n': (0, 1),
    'ne': (1, 1),
    'se': (1, -1),
    's': (0, -1),
    'sw': (-1, -1),
    'nw': (-1, 1)
}


x = 0
y = 0
max_x = 0
max_y = 0
for step in steps:
    dx, dy = deltas[step]
    x += dx
    y += dy
    # print('x = {0}, y = {1}'.format(x, y))
    max_x = max(x, max_x)
    max_y = max(y, max_y)

print('x = {0}, y = {1}'.format(x, y))
print('max x = {0}, max y = {1}'.format(max_x, max_y))
