#!/usr/bin/python

from __future__ import print_function
import sys


def main():

    lines = None    # load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-14.txt'):

    with open(filename, 'r') as handle:
        data = [line.rstrip() for line in handle.readlines()]

    return data


COUNT = 84601


def part1(lines):

    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    for i in range(COUNT+10):
        score = recipes[elf1] + recipes[elf2]
        if score < 10:
            recipes.append(score)
        else:
            recipes.append(score / 10)
            recipes.append(score % 10)
        elf1 += 1 + recipes[elf1]
        elf1 %= len(recipes)
        elf2 += 1 + recipes[elf2]
        elf2 %= len(recipes)

    print(recipes[COUNT:COUNT+10])

    return


def part2(lines):

    recipes = [3, 7]
    value = 37
    elf1 = 0
    elf2 = 1
    iterations = 2
    while True:
        iterations += 1
        score = recipes[elf1] + recipes[elf2]
        if score < 10:
            recipes.append(score)
            value = check_value(value, score, recipes, iterations)

        else:
            recipes.append(score / 10)
            recipes.append(score % 10)
            value = check_value(value, score / 10, recipes, iterations)
            iterations += 1
            value = check_value(value, score % 10, recipes, iterations)

        elf1 += 1 + recipes[elf1]
        elf1 %= len(recipes)
        elf2 += 1 + recipes[elf2]
        elf2 %= len(recipes)

    return


def check_value(value, score, recipes, iterations):

    value *= 10
    value += score
    value %= 1000000
    if value == COUNT:
        print('Found {0} after {1} iterations.'.format(recipes[-6:], iterations - 6))
        sys.exit(0)

    return value


if __name__ == '__main__':
    main()
