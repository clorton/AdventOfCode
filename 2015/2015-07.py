#! /usr/bin/python

import re

"""
This year, Santa brought little Bobby Tables a set of wires and bitwise logic gates! Unfortunately, little Bobby is a little under the recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal (a number from 0 to 65535). A signal is provided to each wire by a gate, another wire, or some specific value. Each wire can only get a signal from one source, but can provide its signal to multiple destinations. A gate provides no signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together: x AND y -> z means to connect wires x and y to an AND gate, and then connect its output to wire z.

For example:

    123 -> x means that the signal 123 is provided to wire x.
    x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.
    p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.
    NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.

Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for some reason, you'd like to emulate the circuit instead, almost all programming languages (for example, C, JavaScript, or Python) provide operators for these gates.

For example, here is a simple circuit:

123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i

After it is run, these are the signals on the wires:

d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456

In little Bobby's kit's instructions booklet (provided as your puzzle input), what signal is ultimately provided to wire a?
"""

class State(object):
    def __init__(self):
        self.state = {}

    def __getitem__(self, key):
        if key.isalpha():
            return self.state[key] if key in self.state else 0
        elif key.isnumeric():
            return int(key)

        raise RuntimeError("Can't return a value for key '{0}'".format(key))

    def __setitem__(self, key, value):
        self.state[key] = value


with open('2015-07.txt', 'r') as handle:
    instructions = handle.readlines()

state = State()
initialize = re.compile('([0-9]+|[a-z]+) -> ([a-z]+)')
invert = re.compile('NOT ([a-z]+) -> ([a-z]+)')
bitwise_and = re.compile('([0-9]+|[a-z]+) AND ([0-9]+|[a-z]+) -> ([a-z]+)')
bitwise_or = re.compile('([0-9]+|[a-z]+) OR ([0-9]+|[a-z]+) -> ([a-z]+)')
left_shift = re.compile('([0-9]+|[a-z]+) LSHIFT ([0-9]+|[a-z]+) -> ([a-z]+)')
right_shift = re.compile('([0-9]+|[a-z]+) RSHIFT ([0-9]+|[a-z]+) -> ([a-z]+)')
for instruction in instructions:

    match = initialize.match(instruction)
    if match:
        source, destination = match.groups()
        state[destination] = state[source]
        continue

    match = invert.match(instruction)
    if match:
        source, destination = match.groups()
        state[destination] = ~state[destination] & 0xFFFF
        continue

    match = bitwise_and.match(instruction)
    if match:
        a, b, destination = match.groups()
        state[destination] = state[a] & state[b]
        continue

    match = bitwise_or.match(instruction)
    if match:
        a, b, destination = match.groups()
        state[destination] = state[a] | state[b]
        continue

    match = left_shift.match(instruction)
    if match:
        source, shift, destination = match.groups()
        state[destination] = state[source] << state[shift]
        continue

    match = right_shift.match(instruction)
    if match:
        source, shift, destination = match.groups()
        state[destination] = state[source] >> state[shift]
        continue

    raise RuntimeError("Unexpected instruction: '{0}'".format(instruction))

print("Value of 'a' = {0}".format(state['a']))
