#!/usr/bin/env python3

from collections import namedtuple


ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
BASE = 9
HALT = 99

POSITION = 0
IMMEDIATE = 1
RELATIVE = 2

Microcode = namedtuple('Microcode', ['function', 'count'])


class Computer(object):

    def __init__(self, memory, inputs=None):
        self.memory = list(memory)
        self.inputs = list(inputs) if inputs is not None else []
        self.ip = 0
        self.index = 0
        self.output = None
        self.base = 0

        return

    def reset(self):
        self.ip = 0

    @classmethod
    def mode(cls, modes, index):
        # modes(1002, 1) => 0
        # modes(1002, 2) => 1
        # modes(1002, 3) => 0
        return (modes // (10**(index+1))) % 10

    def load(self, mode, arg):

        if mode == POSITION:
            while arg >= len(self.memory):
                self.memory.append(0)
            return self.memory[arg]
        elif mode == RELATIVE:
            while (self.base + arg) >= len(self.memory):
                self.memory.append(0)
            return self.memory[self.base + arg]
        elif mode == IMMEDIATE:
            return arg
        else:
            assert False, f"Unknown addressing mode {mode}"

    def store(self, value, mode, location):

        if mode == POSITION:
            while location >= len(self.memory):
                self.memory.append(0)
            self.memory[location] = value
        elif mode == RELATIVE:
            while (self.base + location) >= len(self.memory):
                self.memory.append(0)
            self.memory[self.base + location] = value
        else:
            assert False, f"Cannot store with mode {mode}"

        return

    def add(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        self.store(first + second, Computer.mode(modes, 3), self.memory[self.ip+3])

        return False

    def multiply(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        self.store(first * second, Computer.mode(modes, 3), self.memory[self.ip + 3])

        return False

    def input(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        value = self.inputs[self.index]
        self.index += 1
        self.store(value, Computer.mode(modes, 1), self.memory[self.ip + 1])

        return False

    def output(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        value = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        self.output = value

        return False

    def jump_if_true(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        if first != 0:
            self.ip = second
            return True

        return False

    def jump_if_false(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        if first == 0:
            self.ip = second
            return True

        return False

    def less(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        self.store(1 if first < second else 0, Computer.mode(modes, 3), self.memory[self.ip + 3])

        return False

    def equals(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        self.store(1 if first == second else 0, Computer.mode(modes, 3), self.memory[self.ip + 3])

        return False

    def rebase(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        self.base += first

        return False

    instructions = {
        ADD: Microcode(add, 4),
        MULTIPLY: Microcode(multiply, 4),
        INPUT: Microcode(input, 2),
        OUTPUT: Microcode(output, 2),
        JUMP_IF_TRUE: Microcode(jump_if_true, 3),
        JUMP_IF_FALSE: Microcode(jump_if_false, 3),
        LESS_THAN: Microcode(less, 4),
        EQUALS: Microcode(equals, 4),
        BASE: Microcode(rebase, 2)
    }

    def run(self, inputs=None) -> int:

        if inputs is not None:
            self.inputs = list(inputs)
            self.index = 0
        self.output = None
        while self.memory[self.ip] != HALT:
            opcode = self.memory[self.ip] % 10
            if not Computer.instructions[opcode].function(self):
                self.ip += Computer.instructions[opcode].count
            if opcode == OUTPUT:
                break

        # noinspection PyTypeChecker
        return self.output
