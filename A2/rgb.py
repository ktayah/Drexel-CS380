import random

import agent
import util

DEFAULT_STATE = 'rgrb|grbr|b gr|gbbr'


class Cell:
    EMPTY = ' '
    FORE = {'r': 'white', 'g': 'black', 'b': 'white', ' ': 'white'}
    BACK = {'r': 'red', 'g': 'green', 'b': 'blue', ' ': 'black'}

    @classmethod
    def color(cls, c):
        return util.color_string(c, fore=Cell.FORE[c], back=Cell.BACK[c])


class Action:

    def __init__(self, x, y, x2, y2):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return 'slide({},{},{},{})'.format(self.x, self.y, self.x2, self.y2)


class State:

    def __init__(self, string):
        string = string or DEFAULT_STATE
        self.board = [list(line) for line in string.split('|')]
        self.size = len(self.board)

    def __str__(self):
        return '|'.join([''.join(row) for row in self.board])

    def __eq__(self, state):
        return str(self) == str(state)

    def clone(self):
        return State(str(self))

    def is_legal(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def get(self, x, y):
        return self.board[y][x] if self.is_legal(x, y) else None

    def row(self, y):
        return self.board[y]

    def put(self, x, y, label):
        self.board[y][x] = label

    def is_goal(self):
        for x in range(self.size):
            for y in range(self.size):
                c = self.get(x, y)
                if c != Cell.EMPTY:
                    deltas = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
                    for dx, dy in deltas:
                        x2, y2 = x+dx, y+dy
                        c2 = self.get(x2, y2)
                        if c == c2:
                            return False
        return True

    def actions(self):
        actions = []
        for x in range(self.size):
            for y in range(self.size):
                if self.get(x, y) == Cell.EMPTY:
                    deltas = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
                    for dx, dy in deltas:
                        x2, y2 = x + dx, y + dy
                        if self.is_legal(x2, y2):
                            actions.append(Action(x2, y2, x, y))
        actions.sort(key=lambda action: str(action))
        return actions

    def execute(self, action):
        char = self.get(action.x, action.y)
        self.put(action.x2, action.y2, char)
        self.put(action.x, action.y, Cell.EMPTY)
        return self

    def pprint_string(self):
        top_bottom = util.color_string('+' + ('-' * self.size) + '+',
                                       fore='blue', back='blue')
        side = util.color_string('|', fore='blue', back='blue')
        s = top_bottom + '\n'
        for y in range(self.size):
            s += side + ''.join([Cell.color(c)
                                 for c in self.row(y)]) + side + '\n'
        return s + top_bottom


if __name__ == '__main__':
    cmd = util.get_arg(1)
    if cmd:
        state = State(util.get_arg(2))
        if cmd == 'print':
            util.pprint(state)
        elif cmd == 'goal':
            print(state.is_goal())
        elif cmd == 'actions':
            for action in state.actions():
                print(action)
