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

        return

    @classmethod
    def mode(cls, modes, index):
        # modes(1002, 1) => 0
        # modes(1002, 2) => 1
        # modes(1002, 3) => 0
        return (modes // (10**(index+1))) % 10

    def read(self, mode, arg):

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
        first = self.read(Computer.mode(modes, 1), self.memory[self.ip+1])
        second = self.read(Computer.mode(modes, 2), self.memory[self.ip+2])
        assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(first + second, self.memory[self.ip+3])

        return False

    def multiply(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.read(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.read(Computer.mode(modes, 2), self.memory[self.ip + 2])
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
        value = self.read(Computer.mode(modes, 1), self.memory[self.ip + 1])
        print(f"{value}")

        return False

    def jump_if_true(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.read(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.read(Computer.mode(modes, 2), self.memory[self.ip + 2])
        if first != 0:
            self.ip = second
            return True

        return False

    def jump_if_false(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.read(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.read(Computer.mode(modes, 2), self.memory[self.ip + 2])
        if first == 0:
            self.ip = second
            return True

        return False

    def less(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.read(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.read(Computer.mode(modes, 2), self.memory[self.ip + 2])
        assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(1 if first < second else 0, self.memory[self.ip + 3])

        return False

    def equals(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.read(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.read(Computer.mode(modes, 2), self.memory[self.ip + 2])
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

    def run(self):

        self.ip = 0
        while self.memory[self.ip] != HALT:
            opcode = self.memory[self.ip] % 10
            if not Computer.instructions[opcode].function(self):
                self.ip += Computer.instructions[opcode].count

        return


def main():

    with open("day-05.txt", "r") as file:
        program = [int(value) for value in file.readline().split(",")]

    inputs = [1]

    # # simple test, multiply 33 (from location 4) * 3 and store in location 4
    # program = [1002, 4, 3, 4, 33]
    # inputs = []

    # Part 1

    computer = Computer(program, inputs)
    computer.run()

    # 0
    # 0
    # 0
    # 0
    # 0
    # 0
    # 0
    # 0
    # 0
    # 15259545

    # Part 2

    # # equal to 8, position mode
    # program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    # inputs = [[7], [8], [9]]
    #
    # # less than 8, position mode
    # program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    #
    # # equal to 8, immediate mode
    # program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    #
    # # less than 8, immediate mode
    # program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    #
    # # 0 for 0, 1 for non-zero, position mode
    # program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    # inputs = [[0], [1], [-1], [42]]
    #
    # # 0 for 0, 1 for non-zero, immediate mode
    # program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    #
    # # 999 if input < 8, 1000 if input == 8, 1001 if input > 8
    # program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    # inputs = [[4], [8], [12]]
    #
    # for input in inputs:
    #     computer = Computer(program, input)
    #     computer.run()

    inputs = [5]

    computer = Computer(program, inputs)
    computer.run()

    # 7616021

    return


if __name__ == "__main__":
    main()
