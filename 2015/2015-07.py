#! /usr/bin/python

from functools import reduce
import re

"""
This year, Santa brought little Bobby Tables a set of wires and bitwise logic gates! Unfortunately, little Bobby is a
little under the recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal (a number from 0 to 65535). A signal
is provided to each wire by a gate, another wire, or some specific value. Each wire can only get a signal from one
source, but can provide its signal to multiple destinations. A gate provides no signal until all of its inputs have a
signal.

The included instructions booklet describes how to connect the parts together: x AND y -> z means to connect wires x and
y to an AND gate, and then connect its output to wire z.

For example:

    123 -> x means that the signal 123 is provided to wire x.
    x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.
    p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.
    NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.

Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for some reason, you'd like to emulate the
circuit instead, almost all programming languages (for example, C, JavaScript, or Python) provide operators for these
gates.

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

In little Bobby's kit's instructions booklet (provided as your puzzle input),
what signal is ultimately provided to wire a?
"""


class Component(object):
    def __init__(self):
        pass

    def value(self):
        raise RuntimeError('Not implemented.')


class Constant(Component):
    def __init__(self, constant=None):
        super().__init__()
        self.constant = int(constant)

    def value(self):
        return self.constant

    def __str__(self):
        return str(self.constant)


class Wire(Component):
    def __init__(self, source=None, system=None):
        super().__init__()
        self.source = source
        self.system = system

    def value(self):
        return self.system[self.source].value()

    def __str__(self):
        return self.source


class Not(Component):
    def __init__(self, source=None):
        super().__init__()
        self.source = source

    def value(self):
        return self.source.value() ^ 65535

    def __str__(self):
        return 'NOT {0}'.format(self.source)


class And(Component):
    def __init__(self, sources=list()):
        super().__init__()
        self.sources = sources

    def value(self):
        return reduce(lambda x, y: x & y, [source.value() for source in self.sources])

    def __str__(self):
        return '{0} AND {1}'.format(*self.sources[:2])


class Or(Component):
    def __init__(self, sources=list()):
        super().__init__()
        self.sources = sources

    def value(self):
        return reduce(lambda x, y: x | y, [source.value() for source in self.sources])

    def __str__(self):
        return '{0} OR {1}'.format(*self.sources[:2])


class Left(Component):
    def __init__(self, source=None, amount=0):
        super().__init__()
        self.source = source
        self.amount = amount

    def value(self):
        return self.source.value() << self.amount.value()

    def __str__(self):
        return '{0} << {1}'.format(self.source, self.amount)


class Right(Component):
    def __init__(self, source=None, amount=0):
        super().__init__()
        self.source = source
        self.amount = amount

    def value(self):
        return self.source.value() >> self.amount.value()

    def __str__(self):
        return '{0} >> {1}'.format(self.source, self.amount)


def main():
    with open('2015-07.txt', 'r') as handle:
        instructions = handle.readlines()

    state = {}

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
            if source.isalpha():
                state[destination] = Wire(source, state)
            else:
                state[destination] = Constant(source)
            continue

        match = invert.match(instruction)
        if match:
            source, destination = match.groups()
            source = Wire(source, state) if source.isalpha() else Constant(source)
            state[destination] = Not(source)
            continue

        match = bitwise_and.match(instruction)
        if match:
            a, b, destination = match.groups()
            a = Wire(a, state) if a.isalpha() else Constant(a)
            b = Wire(b, state) if b.isalpha() else Constant(b)
            state[destination] = And([a, b])
            continue

        match = bitwise_or.match(instruction)
        if match:
            a, b, destination = match.groups()
            a = Wire(a, state) if a.isalpha() else Constant(a)
            b = Wire(b, state) if b.isalpha() else Constant(b)
            state[destination] = Or([a, b])
            continue

        match = left_shift.match(instruction)
        if match:
            source, shift, destination = match.groups()
            source = Wire(source, state) if source.isalpha() else Constant(source)
            shift = Wire(shift, state) if shift.isalpha() else Constant(shift)
            state[destination] = Left(source, shift)
            continue

        match = right_shift.match(instruction)
        if match:
            source, shift, destination = match.groups()
            source = Wire(source, state) if source.isalpha() else Constant(source)
            shift = Wire(shift, state) if shift.isalpha() else Constant(shift)
            state[destination] = Right(source, shift)
            continue

        raise RuntimeError("Unexpected instruction: '{0}'".format(instruction))

    print("Value of 'a' = {0}".format(state['a'].value()))

    return


if __name__ == '__main__':
    main()
