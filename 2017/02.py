#!/usr/bin/python

with open('02.txt', 'r') as handle:
    data = [str(line) for line in handle.readlines()]


total = 0

for line in data:
    values = [int(entry) for entry in line.split()]
    diff = max(values) - min(values)
    total += diff

print(total)

total = 0

for line in data:
    values = [int(entry) for entry in line.split()]
    for i in range(len(values)):
        a = values[i]
        for j in range(len(values)):
            b = values[j]
            if (a > b) and ((a % b) == 0):
                print('{0:4} % {1:4} == 0, {0:4} // {1:4} = {2:3}'.format(a, b, a//b))
                total += (a // b)
                break

print(total)
