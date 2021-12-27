#! /usr/bin/env python3

from collections import deque
from pathlib import Path

with Path("../inputs/18.txt").open("r") as handle:
    lines = list([line.strip() for line in handle.readlines()])

splines = [
    "[1,2]",
    "[[1,2],3]",
    "[9,[8,7]]",
    "[[1,9],[8,5]]",
    "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]",
    "[[[9,[3, 8]],[[0,9],6]],[[[3,7],[4,9]],3]]",
    "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]",
]


def reduce(number):

    increase = 0
    explosion = False
    cleavage = False

    def explode(number, stack):

        nonlocal explosion, increase
        explosion = False
        increase = 0
        explode_inner(number, stack, 0)
        return explosion

    def explode_inner(number, stack, depth):

        nonlocal explosion, increase

        if isinstance(number, list):
            left, right = number
            # only one explosion at a time
            if not explosion and (depth == 4):
                for i in range(len(stack)-1, -1, -1):
                    if isinstance(stack[i], int):
                        stack[i] += left
                        break
                stack.append(0)
                increase = right
                explosion = True
            else:
                stack.append("[")
                explode_inner(left, stack, depth+1)
                stack.append(",")
                explode_inner(right, stack, depth+1)
                stack.append("]")
        else:   # digit
            stack.append(number + increase)
            increase = 0

        return

    def split(number, stack):

        nonlocal cleavage
        cleavage = False
        split_inner(number, stack)
        return cleavage

    def split_inner(number, stack):

        nonlocal cleavage

        if isinstance(number, list):
            left, right = number
            stack.append("[")
            split_inner(left, stack)
            stack.append(",")
            split_inner(right, stack)
            stack.append("]")
        else:  # digit
            # only one cleavage at a time
            if not cleavage and (number >= 10):
                stack.extend(["[", number // 2, ",", (number+1) // 2, "]"])
                cleavage = True
            else:
                stack.append(number)

        return

    while True:
        while True:
            stack = []
            save = number
            explode(number, stack)
            number = eval("".join(map(str, stack)))
            if number == save:  # not exploded:
                break
        stack = []
        save = number
        split(number, stack)
        number = eval("".join(map(str, stack)))
        if number == save:  # not cleaved:
            break

    return "".join(map(str, stack))


test_cases = [
    "[[[[[9,8],1],2],3],4]",    # explode [[[[0,9],2],3],4]
    "[7,[6,[5,[4,[3,2]]]]]",    # explode [7,[6,[5,[7,0]]]]
    "[[6,[5,[4,[3,2]]]],1]",    # explode [[6,[5,[7,0]]],3]
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",    # explode x2 [[3,[2,[8,0]]],[9,[5,[7,0]]]]
    "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",    # [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
]

for case in test_cases:
    print(f"{case}: ", end="")
    number = reduce(eval(case))
    print(f"{number=}")
    print()

larger = [
    "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
    "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
    "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
    "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
    "[7,[5,[[3,8],[1,4]]]]",
    "[[2,[2,2]],[8,[8,1]]]",
    "[2,9]",
    "[1,[[[9,3],9],[[9,0],[0,7]]]]",
    "[[[5,[7,4]],7],1]",
    "[[[[4,2],2],6],[8,7]]",
    ]

number = None
for addend in larger:
    if number:
        number = f"[{number},{addend}]"
        number = reduce(eval(number))
    else:
        number = addend


def magnitude(number):

    if isinstance(number, list):
        left, right = number
        return 3*magnitude(left) + 2*magnitude(right)
    else:   # digit
        return number


magnitudes = [
    "[[1,2],[[3,4],5]]",                    #  143
    "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",    # 1384
    "[[[[1,1],[2,2]],[3,3]],[4,4]]",        #  445
    "[[[[3,0],[5,3]],[4,4]],[5,5]]",        #  791
    "[[[[5,0],[7,4]],[5,5]],[6,6]]",        # 1137
    "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"     # 3488
]

for m in magnitudes:
    print(f"{magnitude(eval(m))=}")

examples = [
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

number = examples[0]
for example in examples[1:]:
    number = f"[{number},{example}]"
    number = reduce(eval(number))
print(f"{number=}, {magnitude(eval(number))=}")

number = lines[0]
for line in lines:
    number = f"[{number},{line}]"
    number = reduce(eval(number))
print(f"Part 1: {number=}, {magnitude(eval(number))=}")

maximum = 0
for a in lines:
    for b in lines:
        if a != b:
            maximum = max(maximum, magnitude(eval(reduce(eval(f"[{a},{b}]")))))
            maximum = max(maximum, magnitude(eval(reduce(eval(f"[{b},{a}]")))))
print(f"Part 2: {maximum=}")

pass
