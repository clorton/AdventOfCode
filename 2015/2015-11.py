from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "2015-11.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

line = lines[0]

pwd = np.array([ord(c)-ord("a") for c in line])

def repr(pwd):
    return "".join([chr(ord("a")+c) for c in pwd])

print(repr(pwd))

def increment(pwd):
    for i in range(len(pwd)-1, -1, -1):
        pwd[i] += 1
        if pwd[i] == 26:
            pwd[i] = 0
        else:
            break
    return pwd

# pwd = increment(pwd)
# print(repr(pwd))

# for _ in range(26):
#     pwd = increment(pwd)
# print(repr(pwd))

# for _ in range(26*26):
#     pwd = increment(pwd)
# print(repr(pwd))

def first(pwd):
    count = 0
    for i in range(len(pwd)-2):
        if pwd[i+1] == pwd[i]+1:
            count += 1
            if count == 2:
                return True
        else:
            count = 0
    return False

assert first(np.array([ord(c) for c in "hijklmmn"]))
assert not first(np.array([ord(c) for c in "abbceffg"]))
assert not first(np.array([ord(c) for c in "abbcegjk"]))
assert first(np.array([ord(c) for c in "abcdffaa"]))
assert first(np.array([ord(c) for c in "ghjaabcc"]))

def second(pwd):
    return not any((pwd == ord("i")) | (pwd == ord("o")) | (pwd == ord("l")))

assert not second(np.array([ord(c) for c in "hijklmmn"]))
assert second(np.array([ord(c) for c in "abbceffg"]))
assert second(np.array([ord(c) for c in "abbcegjk"]))
assert second(np.array([ord(c) for c in "abcdffaa"]))
assert second(np.array([ord(c) for c in "ghjaabcc"]))

def third(pwd):
    d = np.diff(pwd)
    return ((d == 0).sum() >= 2) and (len(set(pwd[np.nonzero(d == 0)[0]])) >= 2)

assert not third(np.array([ord(c) for c in "hijklmmn"]))
assert third(np.array([ord(c) for c in "abbceffg"]))
assert not third(np.array([ord(c) for c in "abbcegjk"]))
assert third(np.array([ord(c) for c in "abcdffaa"]))
assert third(np.array([ord(c) for c in "ghjaabcc"]))
assert not third(np.array([ord(c) for c in "ghjaaabc"]))

def valid(pwd):
    return first(pwd) and second(pwd) and third(pwd)

assert not valid(np.array([ord(c) for c in "hijklmmn"]))
assert not valid(np.array([ord(c) for c in "abbceffg"]))
assert not valid(np.array([ord(c) for c in "abbcegjk"]))
assert valid(np.array([ord(c) for c in "abcdffaa"]))
assert valid(np.array([ord(c) for c in "ghjaabcc"]))

while True:
    pwd = increment(pwd)
    if valid(pwd):
        break

print(repr(pwd))

while True:
    pwd = increment(pwd)
    if valid(pwd):
        break

print(repr(pwd))

print("Done.")
