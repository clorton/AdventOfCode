#!/usr/bin/python

from collections import defaultdict
from math import sqrt


class Program(object):
    def __init__(self, instructions, debug):
        self._instructions = instructions
        self._memory = defaultdict(int)
        self._memory['a'] = debug
        self._ip = 0
        self._sends = 0
        self._multiply = 0

        return

    def run(self):

        while True:
            instruction = self._instructions[self._ip]
            command = instruction[0]
            register = instruction[1]
            if len(instruction) > 2:
                argument = instruction[2]
                argument = int(argument) if not argument.isalpha() else self._memory[argument]

            if command == 'set':
                self._memory[register] = argument
                if register == 'h':
                    print('h = {0}'.format(self._memory['h']))
            elif command == 'sub':
                self._memory[register] -= argument
                if register == 'h':
                    print('h = {0}'.format(self._memory['h']))
            elif command == 'mul':
                self._memory[register] *= argument
                self._multiply += 1
                if register == 'h':
                    print('h = {0}'.format(self._memory['h']))
            elif command == 'jnz':
                test = self._memory[register] if register.isalpha() else int(register)
                if test != 0:
                    self._ip += argument - 1
            else:
                raise RuntimeError()

            self._ip += 1

            if (self._ip < 0) or (self._ip >= len(self._instructions)):
                break

        return self._multiply

    @property
    def sends(self):
        return self._sends


def main():

    with open('2017-23.txt', 'r') as handle:
        instructions = [line.strip().split(' ') for line in handle.readlines()]

    program = Program(instructions, 0)
    multiply = program.run()

    print('{0} multipies'.format(multiply))

    """
    int64_t h = 0;
    for (int64_t b = 109900; b <= 126900; b += 17) {
        std::cout << "B = " << b << std::endl;
        for (int64_t d = 2; d <= int(sqrt(b)); ++d) {
            if ((b % d) == 0) {
                std::cout << "Incrementing h" << std::endl;
                ++h;
                break;
            }
        }
    }
    """
    h = 0
    for b in range(109900, 126901, 17):
        for d in range(2, int(sqrt(b))+1):
            if (b % d) == 0:
                h += 1
                break

    print('H is {0}'.format(h))

    return


if __name__ == '__main__':
    main()