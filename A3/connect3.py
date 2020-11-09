import math
import random
import sys

import util


class Cell:
    EMPTY = ' '
    FORE = {'X': 'white', 'O': 'white', ' ': 'white'}
    BACK = {'X': 'red', 'O': 'green', ' ': 'black'}

    @classmethod
    def color(cls, char):
        return util.color_string(char, fore=Cell.FORE[char], back=Cell.BACK[char])


class Action:

    def __init__(self, char, x):
        self.char = char
        self.x = x

    def __str__(self):
        return 'drop({},{})'.format(self.char, self.x)


class State:

    def __init__(self, string=None, connect=3, size_x=4, size_y=3):
        self.connect = connect
        if string:
            self.board = [list(line) for line in string.split('|')]
            self.max_x = len(self.board[0]) if self.board else 0
            self.max_y = len(self.board)
        else:
            self.board = [list(Cell.EMPTY * size_x) for y in range(size_y)]
            self.max_x = size_x
            self.max_y = size_y

    def __str__(self):
        return '|'.join([''.join(row) for row in self.board])

    def __eq__(self, state):
        return str(self) == str(state)

    def clone(self):
        return State(str(self))

    def is_legal(self, x, y):
        return x >= 0 and x < self.max_x and y >= 0 and y < self.max_y

    def get(self, x, y):
        return self.board[y][x] if self.is_legal(x, y) else None

    def row(self, y):
        return self.board[y]

    def put(self, x, y, c):
        self.board[y][x] = c

    def num_empties(self):
        return str(self).count(Cell.EMPTY)

    def first_empty_y(self, x):
        y = self.max_y - 1
        while y >= 0 and self.get(x, y) != Cell.EMPTY:
            y -= 1
        return y if y >= 0 else None

    def drop(self, c, x):
        y = self.first_empty_y(x)
        if y is not None:
            self.put(x, y, c)
        return self

    def equals(self, state):
        return self.compact_string() == state.compact_string()

    def actions(self, char):
        actions = []
        for x in range(self.max_x):
            y = self.first_empty_y(x)
            if y is not None:
                actions.append(Action(char, x))
        return actions

    def execute(self, action):
        self.drop(action.char, action.x)
        return self

    def game_over(self):
        return self.winner() or self.num_empties() == 0

    def _winner_test(self, c, x, y, dx, dy):
        for _ in range(self.connect - 1):
            x += dx
            y += dy
            if self.get(x, y) != c:
                return False
        return True

    def winner(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                c = self.get(x, y)
                if c != Cell.EMPTY:
                    deltas = [(+1, 0), (0, +1), (+1, +1), (-1, +1)]
                    for dx, dy in deltas:
                        if self._winner_test(c, x, y, dx, dy):
                            return c
        return None

    def pprint_string(self):
        top_bottom = util.color_string('+' + ('-' * self.max_x) + '+',
                                       fore='blue', back='blue')
        side = util.color_string('|', fore='blue', back='blue')
        s = ''
        for y in range(self.max_y):
            s += side + ''.join([Cell.color(c)
                                 for c in self.row(y)]) + side + '\n'
        return s + top_bottom


if __name__ == '__main__':
    cmd = util.get_arg(1)
    if cmd:
        if cmd == 'print':
            state = State(util.get_arg(2))
            util.pprint(state)
        elif cmd == 'over':
            state = State(util.get_arg(2))
            print(state.game_over())
        elif cmd == 'winner':
            state = State(util.get_arg(2))
            print(state.winner())
        elif cmd == 'actions':
            char = util.get_arg(2)
            state = State(util.get_arg(3))
            for action in state.actions(char):
                print(action)
