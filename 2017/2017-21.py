#!/usr/bin/python


class Image(object):
    def __init__(self):
        pass


def main():

    with open('2017-21.txt', 'r') as handle:
        data = handle.readlines()

    rules = {}
    for line in data:
        key, value = line.strip().split(' => ')
        rules[key] = value

    image = [
        ['.', '#', '.'],
        ['.', '.', '#'],
        ['#', '#', '#']
    ]

    for i in range(5):
        enhancement = get_blocks(image)
        new_image = []
        for row in enhancement:
            new_row = []
            for col in row:
                for rotation in col:
                    print('Checking {0}'.format(rotation))
                    if rotation in rules:
                        print('{0} => {1}'.format(rotation, rules[rotation]))
                        new_row.append(rules[rotation])
                        break
            new_image.append(new_row)
        image = expand(new_image)

    return


def get_blocks(image):
    if len(image) % 2 == 0:
        blocks = []
        for y in range(0, len(image), 2):
            row = []
            for x in range(0, len(image), 2):
                zero = '/'.join([''.join([image[y+j][x+k] for k in range(2)]) for j in range(2)])
                ninety = '/'.join([''.join([image[y+j][x+k] for j in range(2)]) for k in range(1, -1, -1)])
                one_eighty = ''.join(reversed(zero))
                two_seventy = ''.join(reversed(ninety))

                flip_zero = '/'.join([''.join([image[y + j][x + k] for k in range(1, -1, -1)]) for j in range(2)])
                flip_ninety = '/'.join([''.join([image[y + j][x + k] for j in range(1, -1, -1)]) for k in range(1, -1, -1)])
                flip_one_eighty = ''.join(reversed(flip_zero))
                flip_two_seventy = ''.join(reversed(flip_ninety))

                row.append([zero, ninety, one_eighty, two_seventy, flip_zero, flip_ninety, flip_one_eighty, flip_two_seventy])
            blocks.append(row)
    elif len(image) % 3 == 0:
        blocks = []
        for y in range(0, len(image), 3):
            row = []
            for x in range(0, len(image), 3):
                zero = '/'.join([''.join([image[y+j][x+k] for k in range(3)]) for j in range(3)])
                ninety = '/'.join([''.join([image[y+j][x+k] for j in range(3)]) for k in range(2, -1, -1)])
                one_eighty = ''.join(reversed(zero))
                two_seventy = ''.join(reversed(ninety))

                flip_zero = '/'.join([''.join([image[y+j][x+k] for k in range(2, -1, -1)]) for j in range(3)])
                flip_ninety = '/'.join([''.join([image[y+j][x+k] for j in range(2, -1, -1)]) for k in range(2, -1, -1)])
                flip_one_eighty = ''.join(reversed(flip_zero))
                flip_two_seventy = ''.join(reversed(flip_ninety))

                row.append([zero, ninety, one_eighty, two_seventy, flip_zero, flip_ninety, flip_one_eighty, flip_two_seventy])
            blocks.append(row)
    else:
        raise RuntimeError('Image dimensions {0}'.format(len(image)))

    return blocks


def expand(patterns):

    sample = patterns[0][0]
    dimension = len(patterns)
    height = sample.count('/') + 1
    image = [[] for y in range(height * dimension)]
    for y in range(len(patterns)):
        row = patterns[y]
        for j in range(height):
            for x in range(len(row)):
                image[y+j].extend(row[x].split('/')[j])

    return image


if __name__ == '__main__':
    main()
