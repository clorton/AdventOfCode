#! /usr/bin/env python3

from collections import deque, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-18.txt").read_text()
lines = text.split("\n")
lines = [list(line.replace(" ", "")) for line in lines]
# numbers = [int(string) for string in lines]


# part 1
def matching(line: list) -> int:

    count = 0
    for index, entry in enumerate(line):
        if entry == "(":
            count += 1
        elif entry == ")":
            count -= 1
            if count == 0:
                return index

    raise RuntimeError(f"Could not find matching close parenthesis in '{line}'")


DIGITS = set(list("0123456789"))


def evaluate(line: list) -> int:

    value = 0
    operation = None
    index = 0
    while index < len(line):
        character = line[index]
        if character in DIGITS:
            operand = int(character)
            if operation:
                value = operation(value, operand)
                operation = None
            else:
                value = operand
        elif character == "+":
            operation = lambda x, y: x + y
        elif character == "*":
            operation = lambda x, y: x * y
        elif character == "(":
            close = matching(line[index:])
            operand = evaluate(line[index+1:index+close])
            index += close
            if operation:
                value = operation(value, operand)
                operation = None
            else:
                value = operand
        elif character == ")":
            pass
        else:
            raise RuntimeError(f"Unknown character encountered in '{line}'")
        index += 1

    return value


total = 0
for line in lines:
    total += evaluate(line)

print(f"Total is {total}")


# part 2
def advanced(line: list) -> int:

    expression = line

    while "(" in expression:
        start = expression.index("(")
        close = matching(expression[start:])
        reduced = expression[:start]
        reduced.append(advanced(expression[start+1:start+close]))
        reduced.extend(expression[start+close+1:])
        expression = reduced

    while "+" in expression:
        position = expression.index("+")
        reduced = expression[:position-1]
        reduced.append(expression[position-1] + expression[position+1])
        reduced.extend(expression[position+2:])
        expression = reduced

    total = 1
    for entry in expression:
        if entry != "*":
            total *= entry

    return total


def preprocess(line: list) -> list:
    return list(map(lambda x: int(x) if x in DIGITS else x, line))


# result = advanced(preprocess(list("1+(2*3)+(4*(5+6))")))
# result = advanced(preprocess(list("5*9*(7*3*3+9*3+(8+6*4))")))
total = 0
for line in lines:
    total += advanced(preprocess(line))
print(f"Advanced total is {total}")

print(".oO( done )")
