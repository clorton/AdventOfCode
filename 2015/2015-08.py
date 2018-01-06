#!/usr/bin/python

from enum import Enum


def main():

    strings = get_strings('2015-08.txt')

    literals = 0
    total = 0
    for string in strings:
        literal, memory = process_string(string)
        literals += literal
        total += memory

    print('{0} strings, {1} literal bytes, {2} in memory => {3}'.format(len(strings), literals, total, literals-total))

    # strings = [
    #     '""',
    #     '"abc"',
    #     '"aaa\\"aaa"',
    #     '"\\x27"'
    # ]

    literals = 0
    encoded = 0
    for string in strings:
        literal, encoding = process_string2(string)
        literals += literal
        encoded += encoding

    print('{0} strings, {1} literal characters, {2} characters encoded => {3}'.format(len(strings), literals, encoded, encoded-literals))

    return


def get_strings(filename):

    with open(filename, 'r') as handle:
        strings = [line.strip() for line in handle.readlines()]

    return strings


class State(Enum):
    START = 0
    ESCAPE = 1
    HEX = 2


def process_string(string):

    remaining = 0

    def start(test):
        return (1, State.START) if test != '\\' else (0, State.ESCAPE)

    def escape(test):
        global remaining
        remaining = 2
        return (1, State.START) if test != 'x' else (0, State.HEX)

    def hexadecimal(test):
        global remaining
        remaining -= 1
        return (0, State.HEX) if remaining > 0 else (1, State.START)

    machine = {
        State.START: start,
        State.ESCAPE: escape,
        State.HEX: hexadecimal
    }

    literal = len(string)
    memory = 0
    state = State.START
    for c in string[1:-1]:
        count, state = machine[state](c)
        memory += count

    return literal, memory


def process_string2(string):

    literal = len(string)
    slashes = string.replace('\\', '\\\\')
    quotes = slashes.replace('"', '\\"')
    encoded = len('"' + quotes + '"')

    return literal, encoded


if __name__ == '__main__':
    main()
