#! /usr/bin/env python3

from collections import deque
from pathlib import Path

def get_input(filename: Path) -> tuple:
    text = filename.read_text()
    _ = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
    rules, messages = text.split("\n\n")
    rules = rules.split("\n")
    rules = {int(rule.split(": ")[0]): rule.split(": ")[1].split(" | ") for rule in rules}
    for rule, patterns in rules.items():
        cleaned = []
        for pattern in patterns:
            if pattern == '"a"' or pattern == '"b"':
                cleaned.append(pattern[1])
            else:
                cleaned.append([int(value) for value in pattern.split(" ")])
        rules[rule] = cleaned

    messages = messages.split("\n")

    return rules, messages


def match(rules: deque, message: str) -> bool:

    chars = ["a", "b"]

    def inner(deck, text):

        if len(deck) == 0:
            return len(text) == 0

        if len(text) == 0:
            return False

        rule = deck.popleft()

        if rule in chars:
            if text[0] == rule:
                return inner(deck, text[1:])
            else:
                return False

        for options in rules[rule]:
            temp = deque(deck)
            for pattern in reversed(options):
                temp.appendleft(pattern)
            if inner(temp, text):
                return True

        return False

    stack = deque()
    stack.appendleft(0)

    matched = inner(stack, message)

    return matched


def main():
    rules, messages = get_input(Path("/Users/christopher/Coding/AdventOfCode/2020/day-19.txt"))
    rules[8] = [[42], [42,8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    valid = 0
    for message in messages:
        matched = match(rules, message)
        valid += 1 if matched else 0
    print(f"Found {valid} valid messages.")

    print(".oO('done')")

    return

if __name__ == "__main__":
    main()
