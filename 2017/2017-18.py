#!/usr/bin/python

from collections import defaultdict
from collections import deque


queues = [deque(), deque()]


class Program(object):
    def __init__(self, instructions, pid):
        self._instructions = instructions
        self._pid = pid
        self._memory = defaultdict(int)
        self._memory['p'] = self._pid
        self._ip = 0
        self._sends = 0

        return

    def run(self):
        while True:
            instruction = self._instructions[self._ip]
            command = instruction[0]
            register = instruction[1]
            if len(instruction) > 2:
                argument = instruction[2]
                argument = int(argument) if not argument.isalpha() else self._memory[argument]
            if command == 'snd':
                # sound = self._memory[register]
                queues[1-self._pid].append(self._memory[register])
                self._sends += 1
            elif command == 'set':
                self._memory[register] = argument
            elif command == 'add':
                self._memory[register] += argument
            elif command == 'mul':
                self._memory[register] *= argument
            elif command == 'mod':
                self._memory[register] %= argument
            elif command == 'rcv':
                if len(queues[self._pid]) > 0:
                    self._memory[register] = queues[self._pid].popleft()
                else:
                    break
            elif command == 'jgz':
                test = self._memory[register] if register.isalpha() else int(register)
                if test > 0:
                    self._ip += argument - 1
            else:
                raise RuntimeError()

            self._ip += 1

        return

    @property
    def sends(self):
        return self._sends


def main():

    with open('2017-18.txt', 'r') as handle:
        instructions = [line.strip().split(' ') for line in handle.readlines()]

    memory = defaultdict(int)
    ip = 0
    sound = None
    while True:
        instruction = instructions[ip]
        command = instruction[0]
        register = instruction[1]
        if len(instruction) > 2:
            argument = instruction[2]
            argument = int(argument) if not argument.isalpha() else memory[argument]
        if command == 'snd':
            sound = memory[register]
        elif command == 'set':
            memory[register] = argument
        elif command == 'add':
            memory[register] += argument
        elif command == 'mul':
            memory[register] *= argument
        elif command == 'mod':
            memory[register] %= argument
        elif command == 'rcv':
            if memory[register] != 0:
                print('Last sound frequency was {0}'.format(sound))
                break
        elif command == 'jgz':
            if memory[register] > 0:
                ip += argument - 1
        else:
            raise RuntimeError()
        ip += 1

    # instructions = [
    #     ['set', 'a', '1'],
    #     ['snd', 'a'],
    #     ['add', 'a', '1'],
    #     ['snd', 'a'],
    #     ['set', 'a', '0'],
    #     ['snd', 'p'],
    #     ['rcv', 'a'],
    #     ['rcv', 'b'],
    #     ['rcv', 'c'],
    #     ['rcv', 'd']
    # ]

    program_zero = Program(instructions, 0)
    program_one = Program(instructions, 1)

    program_zero.run()
    program_one.run()
    while (len(queues[0]) > 0) or (len(queues[1]) > 0):
        program_zero.run()
        program_one.run()

    print('Program zero sent {0} times'.format(program_zero.sends))
    print('Program one send {0} times'.format(program_one.sends))

    return


if __name__ == '__main__':
    main()