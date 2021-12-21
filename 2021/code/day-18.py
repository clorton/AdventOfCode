#! /usr/bin/env python3

from collections import deque
from pathlib import Path

with Path("../inputs/18.txt").open("r") as handle:
    # lines = list([eval(line.strip()) for line in handle.readlines()])
    lines = list([line.strip() for line in handle.readlines()])

"""
lines = [
    [1, 2],
    [[1, 2], 3],
    [9, [8, 7]],
    [[1, 9], [8, 5]],
    [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], 9],
    [[[9, [3, 8]], [[0, 9], 6]], [[[3, 7], [4, 9]], 3]],
    [[[[1, 3], [5, 3]], [[1, 3], [8, 7]]], [[[4, 9], [6, 9]], [[8, 2], [7, 3]]]],
]
"""

test_cases = [
    "[[[[[9,8],1],2],3],4]",    # explode [[[[0,9],2],3],4]
    "[7,[6,[5,[4,[3,2]]]]]",    # explode [7,[6,[5,[7,0]]]]
    "[[6,[5,[4,[3,2]]]],1]",    # explode [[6,[5,[7,0]]],3]
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",    # explode x2 [[3,[2,[8,0]]],[9,[5,[7,0]]]]
    "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",    # [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
]

example = [
    "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
    "[[[5,[2,8]],4],[5,[[9,9],0]]]",
    "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
    "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
    "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
    "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
    "[[[[5,4],[7,7]],8],[[8,3],8]]",
    "[[9,3],[[9,9],[6,[4,9]]]]",
    "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
    "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
]   # [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]] = 4140


class Number:

    def __init__(self, value):
        self.value = value
        return

    def __int__(self):
        return self.value

    def __str__(self):
        return f"{self.value}"


def inorder(number, stack, depth=0):

    if isinstance(number, list):
        left, right = number
        _ = inorder(left, stack, depth+1)
        stack.append((number, depth))
        _ = inorder(right, stack, depth+1)
    else:
        pass
        # stack.append((number, depth))

    return stack


def add_snailfish(left, right):

    return [left, right]


test = eval(test_cases[0])


def visit(number):

    to_visit = [number]
    visited = []

    while len(to_visit):

        number = to_visit.pop()
        if len(to_visit) == 4:     # explode
            assert isinstance(number, list)
            add_left, add_right = number
            assert isinstance(add_left, int)
            assert isinstance(add_right, int)
            break

        if isinstance(number, list):
            visited.append(number)
            left, right = number
            to_visit.append(right)
            to_visit.append(left)
        else:
            pass    # integer

    # traverse backward, add_left to next number
    # continue forward, add_right to next number

    return


stack = inorder(test, [])
stack = list(filter(lambda e: isinstance(e[0], list), stack))
test = eval("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
stack = inorder(test, [])
stack = list(filter(lambda e: isinstance(e[0], list), stack))
visit(test)

for test_case in test_cases:
    stack = inorder(eval(test_case), [])

pass
