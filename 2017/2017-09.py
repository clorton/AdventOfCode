#!/usr/bin/python


def main():

    with open('2017-09.txt', 'r') as handle:
        stream = handle.readline()

    groups, score, garbage = process_stream(stream)

    print('{0} groups with total score {1} and {2} garbage characters'.format(groups, score, garbage))

    return


def process_stream(stream):
    total_groups = 0
    score = 0
    total_score = 0
    ignore = False
    garbage = False
    garbage_count = 0

    for char in stream:
        if not ignore:
            if not garbage:
                if char == '{':
                    score += 1
                if char == '!':
                    ignore = True
                if char == '}':
                    total_groups += 1
                    total_score += score
                    score -= 1
                if char == '<':
                    garbage = True
            else:
                if char == '!':
                    ignore = True
                elif char == '>':
                    garbage = False
                else:
                    garbage_count += 1
        else:
            ignore = False

    return total_groups, total_score, garbage_count


if __name__ == '__main__':
    main()
