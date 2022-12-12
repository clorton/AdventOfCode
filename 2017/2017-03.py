#! /usr/bin/python

"""
You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the location of the only access port for this memory system) by programs that can only move up, down, left, or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

    Data from square 1 is carried 0 steps, since it's at the access port.
    Data from square 12 is carried 3 steps, such as: down, left, left.
    Data from square 23 is carried only 2 steps: up twice.
    Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?

Your puzzle input is 289326.
"""

"""
ring  up    left  down  right
  0     0     0     0     1
  1     1     2     2     3
  2     3     4     4     5
  3     5     6     6     7
"""


def spiral(target):
    x = 0
    y = 0
    current = 1
    ups = 0
    lefts = 0
    downs = 0
    rights = 0
    up = 0
    left = 0
    down = 0
    right = 1
    while current < target:
        if ups < up:
            y += 1
            ups += 1
        elif lefts < left:
            x -= 1
            lefts += 1
        elif downs < down:
            y -= 1
            downs += 1
        elif rights < right:
            x += 1
            rights += 1

        if rights == right:
            if current == 1:
                up += 1
            else:
                up += 2
            left += 2
            down += 2
            right += 2
            ups, lefts, downs, rights = 0, 0, 0, 0

        current += 1

        # print('index {0:6} at ({1:4}, {2:4}) = {3:3}'.format(index, x_coord, y_coord, abs(x_coord) + abs(y_coord)))

    return x, y


index = 289326
x_coord, y_coord = spiral(index)
print('index {0:6} at ({1:4}, {2:4}) = {3:3}'.format(index, x_coord, y_coord, abs(x_coord) + abs(y_coord)))

"""
As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

    Square 1 starts with the value 1.
    Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
    Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
    Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
    Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.

Once a square is written, its value does not change. Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?

Your puzzle input is still 289326.
"""


class Row(object):
    def __init__(self, dimension=1024):
        self._dimension = dimension
        self._middle = dimension // 2
        self._row = [0] * dimension

    def __getitem__(self, item):
        return self._row[item + self._middle]

    def __setitem__(self, key, value):
        self._row[key + self._middle] = value


class Memory(object):
    def __init__(self, dimension=1024):
        self._dimension = dimension
        self._middle = dimension // 2
        self._ram = [Row(dimension) for i in range(dimension)]

    def __getitem__(self, item):
        return self._ram[item + self._middle]

    def __setitem__(self, key, value):
        raise RuntimeError("Can't set memory rows.")

    def __delitem__(self, key):
        raise RuntimeError("Can't delete memory rows.")


# index 289326 at (-150,  269) = 419
ram = Memory(101)


def addresses():
    x = 0
    y = 0
    current = 1
    ups = 0
    lefts = 0
    downs = 0
    rights = 0
    up = 0
    left = 0
    down = 0
    right = 1
    while True:
        if ups < up:
            y += 1
            ups += 1
        elif lefts < left:
            x -= 1
            lefts += 1
        elif downs < down:
            y -= 1
            downs += 1
        elif rights < right:
            x += 1
            rights += 1

        if rights == right:
            if current == 1:
                up += 1
            else:
                up += 2
            left += 2
            down += 2
            right += 2
            ups, lefts, downs, rights = 0, 0, 0, 0

        current += 1

        # print('index {0:6} at ({1:4}, {2:4}) = {3:3}'.format(current, x_coord, y_coord, abs(x_coord) + abs(y_coord)))
        yield x, y


offsets = [
    (-1, 1), (0, 1), (1, 1),
    (-1, 0), (1, 0),
    (-1, -1), (0, -1), (1, -1)
]

ram[0][0] = 1
for x, y in addresses():
    total = 0
    for dx, dy in offsets:
        ix = x + dx
        iy = y + dy
        value = ram[iy][ix]
        print('Read  {value:6} from ({x:3},{y:3})'.format(value=value, x=ix, y=iy))
        total += value
    ram[y][x] = total
    print('Wrote {total:6} to   ({x:3},{y:3})'.format(total=total, x=x, y=y))
    if total > 265149:   # 289326:
        print('Wrote memory value {0}'.format(total))
        break
