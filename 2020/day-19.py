#! /usr/bin/env python3

from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-19.txt").read_text()

test = """0: 4 1 5
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

text = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""


rules, messages = text.split("\n\n")
rules = rules.split("\n")
rules = {int(rule.split(": ")[0]): rule.split(": ")[1] for rule in rules}
for rule, pattern in rules.items():
    if "|" in pattern:
        pattern = pattern.split(" | ")
        pattern[0] = [int(rule) for rule in pattern[0].split(" ")]
        pattern[1] = [int(rule) for rule in pattern[1].split(" ")]
    elif '"' in pattern:
        pattern = pattern[1]
    else:
        pattern = [[int(rule) for rule in pattern.split(" ")]]
    rules[rule] = pattern

messages = messages.split("\n")

DEBUG = False


def apply(rule, rules, message):

    if rules[rule] in ["a", "b"]:
        if message:
            print(f"'{message}' {'matched' if message[0] == rules[rule] else 'did NOT match'} rule {rule} ('{rules[rule]}')") if DEBUG else None
            return message[0] == rules[rule], 1
        else:
            print(f"message empty trying to match rule {rule} ('{rules[rule]}')") if DEBUG else None
            return False, 0
    else:
        print(f"Testing patterns in rule {rule} - {rules[rule]}") if DEBUG else None
        for pattern in rules[rule]:
            test = message
            matches = True
            total = 0
            for sub in pattern:
                match, length = apply(sub, rules, test)
                if match:
                    test = test[length:]
                    total += length
                else:
                    matches = False
                    break
            if matches:
                return True, total
        return False, 0

    raise RuntimeError("Exited if/else?")


def part1(messages, rules):
    global DEBUG
    matching = 0
    # matched, length = apply(0, rules, messages[0])
    for index, message in enumerate(messages):
        # DEBUG = (index == 3)
        matched, length = apply(0, rules, message)
        matched &= length == len(message)
        matching += 1 if matched else 0
        print(f"{message} is {'valid' if matched else 'invalid'}")

    print(f"Found {matching} valid messages.")

    return


# part1(messages, rules)


def part2(messages, rules):
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    part1(messages, rules)

    return


part2(messages, rules)


print(".oO( done )")
