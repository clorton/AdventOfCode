#!/usr/bin/env python3



from collections import namedtuple
from itertools import permutations

ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99

POSITION = 0
IMMEDIATE = 1

Microcode = namedtuple('Microcode', ['function', 'count'])


class Computer(object):

    def __init__(self, memory, inputs):
        self.memory = list(memory)
        self.inputs = list(inputs)
        self.ip = 0
        self.index = 0
        self.output = None

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
            return self.memory[arg]
        elif mode == IMMEDIATE:
            return arg
        else:
            assert False, f"Unknown addressing mode {mode}"

    def store(self, value, location):

        self.memory[location] = value

        return

    def add(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(first + second, self.memory[self.ip+3])

        return False

    def multiply(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(first * second, self.memory[self.ip + 3])

        return False

    def input(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        value = self.inputs[self.index]
        self.index += 1
        assert Computer.mode(modes, 1) == POSITION, 'Cannot store with immediate mode.'
        self.store(value, self.memory[self.ip + 1])

        return False

    def output(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        value = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        self.output = value
        # print(f"value")

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
        assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(1 if first < second else 0, self.memory[self.ip + 3])

        return False

    def equals(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(1 if first == second else 0, self.memory[self.ip + 3])

        return False

    instructions = {
        ADD: Microcode(add, 4),
        MULTIPLY: Microcode(multiply, 4),
        INPUT: Microcode(input, 2),
        OUTPUT: Microcode(output, 2),
        JUMP_IF_TRUE: Microcode(jump_if_true, 3),
        JUMP_IF_FALSE: Microcode(jump_if_false, 3),
        LESS_THAN: Microcode(less, 4),
        EQUALS: Microcode(equals, 4)
    }

    def run(self, inputs=None):

        if inputs is not None:
            self.inputs.extend(inputs)
        self.output = None
        while self.memory[self.ip] != HALT:
            opcode = self.memory[self.ip] % 10
            if not Computer.instructions[opcode].function(self):
                self.ip += Computer.instructions[opcode].count
            if opcode == OUTPUT:
                break

        return self.output


def test(phases, program):

    inputs = [[phases[i]] for i in range(5)]
    amplifiers = [Computer(program, inputs[i]) for i in range(5)]
    output = 0
    for index in range(5):
        output = amplifiers[index].run([output])

    return output


def feedback(phases, program):

    inputs = [[phases[i]] for i in range(5)]
    amplifiers = [Computer(program, inputs[i]) for i in range(5)]
    index = 0
    output = 0
    last = None
    while output is not None:
        last = output
        output = amplifiers[index].run([output])
        index = (index + 1) % 5

    return last


def main():

    # with open('day-07.txt', 'r') as file:
    #     inputs = file.readlines()
    #
    # inputs = [entry.strip() for entry in inputs]

    program = [int(entry) for entry in "3,8,1001,8,10,8,105,1,0,0,21,38,55,80,97,118,199,280,361,442,99999,3,9,101,2,9,9,1002,9,5,9,1001,9,4,9,4,9,99,3,9,101,5,9,9,102,2,9,9,1001,9,5,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,101,4,9,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,3,9,9,4,9,99,3,9,101,5,9,9,1002,9,2,9,101,3,9,9,1002,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99".split(",")]

    # program = [int(entry) for entry in "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(",")]
    # program = [int(entry) for entry in "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0".split(",")]
    # program = [int(entry) for entry in "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0".split(",")]

    max = 0
    for permutation in permutations([0, 1, 2, 3, 4]):
        phases = list(permutation)
        signal = test(phases, program)
        if signal > max:
            max = signal
            best = list(phases)

    print(f"Best phase settings are {best} with value {max}.")

    # Part 2

    # program = [int(entry) for entry in "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(",")]
    # program = [int(entry) for entry in "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10".split(",")]

    max = 0
    for permutation in permutations([5, 6, 7, 8, 9]):
        phases = list(permutation)
        signal = feedback(phases, program)
        if signal > max:
            max = signal
            best = list(phases)

    print(f"Best phase settings are {best} with value {max}.")

    return


if __name__ == "__main__":
    main()
