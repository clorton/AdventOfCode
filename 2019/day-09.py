#!/usr/bin/env python3


from collections import namedtuple
from intcode import Computer


def main():

    with open('day-09.txt', 'r') as file:
        data = file.read()

    program = [int(x) for x in data.split(',')]

    # program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    # program = [1102,34915192,34915192,7,4,7,99,0]
    # program = [104,1125899906842624,99]

    c = Computer(program, [1])
    output = c.run()
    while output is not None:
        print(output)
        output = c.run()

    c = Computer(program, [2])
    output = c.run()
    while output is not None:
        print(output)
        output = c.run()

    return


if __name__ == "__main__":
    main()
