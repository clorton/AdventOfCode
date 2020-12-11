#! /usr/bin/env python3


def add(ip, memory):

    a = memory[memory[ip]]
    ip += 1
    b = memory[memory[ip]]
    ip += 1
    destination = memory[ip]
    ip += 1
    memory[destination] = a + b

    return ip


def multiply(ip, memory):

    a = memory[memory[ip]]
    ip += 1
    b = memory[memory[ip]]
    ip += 1
    destination = memory[ip]
    ip += 1
    memory[destination] = a * b

    return ip


opcodes = {
    1: add,
    2: multiply
}


def process(opcode, ip, memory):

    if opcode in opcodes:
        ip = opcodes[opcode](ip, memory)
    else:
        raise RuntimeError(f'Unknown opcode {opcode} at ip {ip}.')

    return ip


def execute(memory):

    ip = 0
    while memory[ip] != 99:
        opcode = memory[ip]
        ip += 1
        ip = process(opcode, ip, memory)

    return memory


def main():

    execute([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    execute([1, 0, 0, 0, 99])
    execute([2, 3, 0, 3, 99])
    execute([2, 4, 4, 5, 99, 0])
    execute([1, 1, 1, 4, 99, 5, 6, 0, 99])

    with open('day-02.txt', 'r') as file:
        line = file.readline().strip()

    memory = line.split(',')
    memory = [int(entry) for entry in memory]

    NOUN = 1
    VERB = 2

    # part 1
    runtime = list(memory)
    runtime[NOUN] = 12
    runtime[VERB] = 2
    execute(runtime)
    print(f'Value at position 0 is {runtime[0]}.')  # 250673 :( needed to initialize memory
                                                    # 5110675 :)

    # part 2

    TARGET = 19690720

    for noun in range(100):
        for verb in range(100):

            runtime = list(memory)
            runtime[NOUN] = noun
            runtime[VERB] = verb

            try:
                execute(runtime)
            except RuntimeError as re:
                print(f'Noun {noun} and verb {verb} were invalid.')

            if runtime[0] == TARGET:
                break
        if runtime[0] == TARGET:
            break

    print(f'Noun {noun} and verb {verb} returned {runtime[0]}, program is {100*noun+verb}.')
    # 4847

    return


if __name__ == '__main__':
    main()
