#!/usr/bin/python

with open('day-01-input.txt', 'r') as handle:
    data = handle.read()

data = str(data)


def get_next_one(string, index):
    return string[(index+1) % len(string)]


total = 0
for i in range(len(data)):
    if data[i] == get_next_one(data, i):
        total += int(data[i])

print(total)


def get_next_half(string, index):
    return string[(index + (len(string) // 2)) % len(string)]


total = 0
for i in range(len(data)):
    if data[i] == get_next_half(data, i):
        total += int(data[i])

print(total)
