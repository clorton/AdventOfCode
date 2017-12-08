#!/usr/bin/python

from collections import defaultdict
import operator
import re

with open('08.txt', 'r') as handle:
    lines = handle.readlines()

operations = {
    'inc': operator.add,
    'dec': operator.sub
}

predicates = {
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

state = defaultdict(int)
pattern = re.compile('([a-z]+) (inc|dec) ([\-0-9]+) if ([a-z]+) ([!=<>]+) ([\-0-9]+)')
highest = 0
for line in lines:
    destination, operation, amount, test, predicate, value = pattern.match(line).groups()
    amount = int(amount)
    value = int(value)
    state[destination] = operations[operation](state[destination], amount) if predicates[predicate](state[test], value) else state[destination]
    highest = max(state[destination], highest)

maximum = max([state[register] for register in state])
print('maximum value is {0}'.format(maximum))
print('highest value held is {0}'.format(highest))
