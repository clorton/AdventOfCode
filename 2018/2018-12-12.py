#!/usr/bin/python

from __future__ import print_function


def main():

    lines = load_data()
    part1(lines)
    part2(lines)

    return


def load_data(filename='2018-12-12.txt'):

    with open(filename, 'r') as handle:
        data = [line.strip() for line in handle.readlines()]

    return data


def part1(lines):

    value = run(20)
    print('Final score: {0}'.format(value))

    return


def part2(lines):

    # pattern doesn't change after generation 111, just shifts right
    onetwentyfour = run(124)
    onetwentyfive = run(125)
    ultimate = ((50000000000 - 125) * (onetwentyfive - onetwentyfour)) + onetwentyfive
    print('Final score: {0}'.format(ultimate))

    return


def run(generations):

    rules = {
        ".....": '.',
        "....#": '.',
        "...#.": '.',
        "...##": '#',
        "..#..": '.',
        "..#.#": '.',
        "..##.": '.',
        "..###": '#',
        ".#...": '#',
        ".#..#": '.',
        ".#.#.": '#',
        ".#.##": '#',
        ".##..": '.',
        ".##.#": '.',
        ".###.": '.',
        ".####": '.',
        "#....": '.',
        "#...#": '#',
        "#..#.": '#',
        "#..##": '#',
        "#.#..": '.',
        "#.#.#": '.',
        "#.##.": '#',
        "#.###": '.',
        "##...": '.',
        "##..#": '#',
        "##.#.": '#',
        "##.##": '.',
        "###..": '#',
        "###.#": '#',
        "####.": '.',
        "#####": '#'
    }

    state = '##.#..#.#..#.####.#########.#...#.#.#......##.#.#...##.....#...#...#.##.#...##...#.####.##..#.#..#.'
    margin = generations + 5
    state = '.'*margin + state + '.'*margin
    print(' 0: {0}'.format(state))
    for step in range(generations):
        subsequent = ['.' for _ in range(len(state))]
        for i in range(len(state)-4):
            pattern = state[i:i+5]
            if pattern in rules:
                rule = rules[pattern]
                subsequent[i+2] = rule
            else:
                print('pattern {0} not found'.format(pattern))
        state = ''.join(subsequent)
        value = score(state, margin)
        print('{0:2} ({2}): {1}'.format(step+1, state, value))

    return value


def score(state, margin):

    value = 0
    for i in range(len(state)):
        if state[i] == '#':
            value += i - margin

    return value


if __name__ == '__main__':
    main()
