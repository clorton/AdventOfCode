#!/usr/bin/python

import re

"""
Because your neighbors keep defeating you in the holiday house decorating contest year after year,
you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed you instructions on how
to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at each corner are at
0,0, 0,999, 999,999, and 999,0. The instructions include whether to turn on, turn off, or toggle
various inclusive ranges given as coordinate pairs. Each coordinate pair represents opposite corners
of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers to 9 lights in a
3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by doing the instructions
Santa sent you in order.

For example:

    turn on 0,0 through 999,999 would turn on (or leave on) every light.
    toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning off the ones that
    were on, and turning on the ones that were off.
    turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.

After following the instructions, how many lights are lit?
"""

with open('2015-06.txt', 'r') as handle:
    instructions = handle.readlines()

lights = [[0] * 1000 for j in range(1000)]

on = re.compile('turn on ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)')
off = re.compile('turn off ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)')
toggle = re.compile('toggle ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)')
for instruction in instructions:
    if instruction.startswith('turn on'):
        x1, y1, x2, y2 = [int(group) for group in on.match(instruction).groups()]
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                lights[y][x] = 1
    elif instruction.startswith('turn off'):
        x1, y1, x2, y2 = [int(group) for group in off.match(instruction).groups()]
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                lights[y][x] = 0
    elif instruction.startswith('toggle'):
        x1, y1, x2, y2 = [int(group) for group in toggle.match(instruction).groups()]
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                lights[y][x] = 1 - lights[y][x]
    else:
        raise RuntimeError("Unrecognized instruction: '{0}'".format(instruction))

lights_on = sum([sum(row) for row in lights])
print('Lights on = {0}'.format(lights_on))

"""
You just finish implementing your winning light pattern when you realize you mistranslated Santa's
message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each light can have a
brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of those lights by 1.

The phrase turn off actually means that you should decrease the brightness of those lights by 1, to a
minimum of zero.

The phrase toggle actually means that you should increase the brightness of those lights by 2.

What is the total brightness of all lights combined after following Santa's instructions?

For example:

    turn on 0,0 through 0,0 would increase the total brightness by 1.
    toggle 0,0 through 999,999 would increase the total brightness by 2000000.
"""

lights = [[0] * 1000 for j in range(1000)]

for instruction in instructions:
    if instruction.startswith('turn on'):
        x1, y1, x2, y2 = [int(group) for group in on.match(instruction).groups()]
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                lights[y][x] += 1
    elif instruction.startswith('turn off'):
        x1, y1, x2, y2 = [int(group) for group in off.match(instruction).groups()]
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                lights[y][x] -= 1 if lights[y][x] > 0 else 0
    elif instruction.startswith('toggle'):
        x1, y1, x2, y2 = [int(group) for group in toggle.match(instruction).groups()]
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                lights[y][x] += 2
    else:
        raise RuntimeError("Unrecognized instruction: '{0}'".format(instruction))

brightness = sum([sum(row) for row in lights])
print('Light brightness = {0}'.format(brightness))
