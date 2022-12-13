#!/usr/bin/env python3

from collections import namedtuple
from pathlib import Path

WORKDIR = Path(__file__).parent.absolute()

Layer = namedtuple('Layer', ['depth', 'location', 'delta'])


def main():

    data = get_input()
    layers = [[int(value.strip()) for value in layer.split(':')] for layer in data]
    count = layers[-1][0] + 1
    firewall = [Layer(0, 0, 0) for i in range(count)]
    for layer, depth in layers:
        firewall[layer] = Layer(depth, 0, 1)

    index = 0
    severity = 0
    for step in range(count):
        severity += check_severity(index, firewall)
        step_firewall(firewall)
        index += 1

    print('Severity of the trip is {0}'.format(severity))

    # layers = [
    #     [0,3],
    #     [1,2],
    #     [4,4],
    #     [6,4]
    # ]
    # count = 7

    delay = 1
    while True:
        penalty = False
        for index, depth in layers:
            test = delay + index
            modulo = (depth - 1) * 2
            if test % modulo == 0:
                # print('First penalty at layer {0} for delay {1}'.format(index, delay))
                penalty = True
                break
        if not penalty:
            print('No penalty for delay {0}'.format(delay))
            break
        delay += 1

    return


def get_input(filename=Path(WORKDIR / '2017-13.txt')):
    with filename.open("r") as handle:
        data = handle.readlines()

    return data


def step_firewall(firewall):
    for i in range(len(firewall)):
        layer = firewall[i]
        if layer.depth > 0:
            location = layer.location + layer.delta
            delta = layer.delta
            if location == firewall[i].depth - 1:
                delta = -1
            elif location == 0:
                delta = 1
            firewall[i] = Layer(layer.depth, location, delta)

    return


def check_severity(index, firewall):
    if (firewall[index].depth > 0) and (firewall[index].location == 0):
        severity = index * firewall[index].depth
        print('Incurred penalty of {0} at layer {1}'.format(severity, index))
        return severity

    return 0


if __name__ == '__main__':
    main()
