"""Solution for Advent of Code 2022 Day 21 Challenge"""

# from collections import namedtuple
from math import isnan, nan
from numbers import Number
from pathlib import Path
from typing import List

# import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / "2022-21.txt"

def get_inputs(filename:Path = INPUTFILE) -> List[str]:

    """Read inputs from given filename."""

    with filename.open("r") as file:
        inputs = [line.strip() for line in file.readlines()]

    # test = [
    #     "root: pppw + sjmn",
    #     "dbpl: 5",
    #     "cczh: sllz + lgvd",
    #     "zczc: 2",
    #     "ptdq: humn - dvpt",
    #     "dvpt: 3",
    #     "lfqf: 4",
    #     "humn: 5",
    #     "ljgn: 2",
    #     "sjmn: drzm * dbpl",
    #     "sllz: 4",
    #     "pppw: cczh / lfqf",
    #     "lgvd: ljgn * ptdq",
    #     "drzm: hmdt - zczc",
    #     "hmdt: 32",
    # ]
    # inputs = test

    print(f"{inputs[0:8]=}")

    return inputs


def main(do_part1:bool=True, do_part2:bool=True) -> None:

    """Docstring"""

    if do_part1:

        part1()

    if do_part2:

        part2()

    # return


def part1() -> None:

    """Docstring"""

    inputs = get_inputs()
    monkeys = {}
    for monkey in inputs:
        name, number = monkey.split(": ")
        if number.isnumeric():
            monkeys[name] = eval(f"lambda m: {int(number)}")
        else:
            arg1, operation, arg2 = number.split(" ")
            monkeys[name] = eval(f"lambda m: m['{arg1}'](m) {operation} m['{arg2}'](m)")

    print(f"Part 1: root={monkeys['root'](monkeys)}")

    # return


def part2() -> None:

    """Docstring"""

    inputs = get_inputs()
    monkeys = {}
    for monkey in inputs:
        name, number = monkey.split(": ")
        if number.isnumeric():
            monkeys[name] = int(number) if name != "humn" else nan
        else:
            monkeys[name] = tuple(number.split(" "))

    def calculable(value) -> bool:

        return isinstance(value, Number) and not isnan(value)

    fix_up = True
    while fix_up:
        fix_up = False
        for key, value in monkeys.items():
            if isinstance(value, tuple):
                if calculable(monkeys[value[0]]) and calculable(monkeys[value[2]]):
                    monkeys[key] = eval(f"{monkeys[value[0]]} {value[1]} {monkeys[value[2]]}")
                    fix_up = True

    def value_of(value, monkeys):

        if value == 'humn':
            return 'humn'
        if isinstance(value, Number):
            return int(value)
        if isinstance(value, str):
            return value_of(monkeys[value], monkeys)

        return (value_of(value[0], monkeys),value[1],value_of(value[2], monkeys))

    root = (monkeys["root"][0], "==", monkeys["root"][2])
    root = value_of(root, monkeys)

    lhs = root[0]
    rhs = root[2]

    while lhs != 'humn':

        operation = lhs[1]

        if isinstance(lhs[0], Number):
            rhs = {
                "+": lambda rhs, arg: rhs - arg,
                "-": lambda rhs, arg: arg - rhs,
                "*": lambda rhs, arg: rhs // arg,
                # "/": lambda rhs, arg: rhs * arg,
            }[operation](rhs, lhs[0])
            lhs = lhs[2]
        elif isinstance(lhs[2], Number):
            rhs = {
                "+": lambda rhs, arg: rhs - arg,
                "-": lambda rhs, arg: rhs + arg,
                "*": lambda rhs, arg: rhs // arg,
                "/": lambda rhs, arg: rhs * arg,
            }[operation](rhs, lhs[2])
            lhs = lhs[0]
        else:
            raise RuntimeError

    print(f"Part 2: {lhs} == {rhs}")

    # return


if __name__ == "__main__":
    main(True, True)
