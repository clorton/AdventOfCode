#! /usr/bin/env python3

from functools import partial
from pathlib import Path

with Path("../inputs/10.txt").open("r") as handle:
    lines = list([list(line.strip()) for line in handle.readlines()])

# lines = [
#     list("[({(<(())[]>[[{[]{<()<>>"),
#     list("[(()[<>])]({[<{<<[]>>("),
#     list("{([(<{}[<>[]}>{[]{[(<()>"),
#     list("(((({<>}<{<{<>}{[]{[]{}"),
#     list("[[<[([]))<([[{}[[()]]]"),
#     list("[{[{({}]{}}([{[{{{}}([]"),
#     list("{<[[]]>}<{[{[{[]{()[[[]"),
#     list("[<(<(<(<{}))><([]([]()"),
#     list("<{([([[(<>()){}]>(<<{{"),
#     list("<{([{{}}[<[[[<>{}]]]>[]]"),
# ]


def push(liszt, delimiter):
    liszt.append(delimiter)
    return None


def pop(liszt, delimiter):
    expected = liszt.pop()
    return None if expected == delimiter else delimiter


operations = {
    "(": partial(push, delimiter=")"),
    "[": partial(push, delimiter="]"),
    "{": partial(push, delimiter="}"),
    "<": partial(push, delimiter=">"),
    ")": partial(pop, delimiter=")"),
    "]": partial(pop, delimiter="]"),
    "}": partial(pop, delimiter="}"),
    ">": partial(pop, delimiter=">"),
}


def part_one(inputs):
    illegal = []
    for line in inputs:
        stack = []
        for delimiter in line:
            result = operations[delimiter](stack)
            if result:
                illegal.append(result)

    values = {")": 3, "]": 57, "}": 1197, ">": 25137}
    points = list(map(lambda c: values[c], illegal))
    print(f"{sum(points)=}")

    return


part_one(lines)


def complete(line):

    stack = []
    for delimiter in line:
        result = operations[delimiter](stack)
        if result:
            return None

    return stack[-1::-1]


def score(suffix):

    points = {")": 1, "]": 2, "}": 3, ">": 4}
    total = 0
    for delimiter in suffix:
        total *= 5
        total += points[delimiter]

    return total


scores = []
for line in lines:
    completion = complete(line)
    scores.append(score(completion)) if completion else None

scores = sorted(scores)
print(f"{scores[len(scores) // 2]=}")

pass
