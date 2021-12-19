#! /usr/bin/env python3

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


def inorder(number, depth=0, stack=None):

    if stack is None:
        stack = []

    if isinstance(number, list):
        left, right = number
        _ = inorder(left, depth+1, stack)
        stack.append((number, depth))
        _ = inorder(right, depth+1, stack)
    else:
        stack.append((number, depth))

    return stack


def add_snailfish(left, right):

    return [left, right]


for test_case in test_cases:
    stack = inorder(test_case)

pass
