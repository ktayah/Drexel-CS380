
class State:
    '''Representation for a game state'''

    # possible actions: up, down, left, right, none
    ACTIONS = ['u', 'd', 'l', 'r', '_']

    def __init__(self, string):
        '''Initializes the state given the API string passed from the game engine'''
        parts = string.split('$')

        # the game screen is represented as a 2d array
        self.screen = [list(line) for line in parts[0].split('|')]

        # max_x, max_y provide the maximum size of the screen
        self.max_y = len(self.screen)
        self.max_x = len(self.screen[0])

        # frog_x, frog_y provide the position of the frog
        index = parts[0].replace('|', '').index('F')
        self.frog_x = index % self.max_x
        self.frog_y = index // self.max_x

        # at_goal is True when the frog has reached the goal row
        self.at_goal = (parts[1].startswith('goal'))

        # score is the number of points awarded to the frog for reaching
        # the goal row (or 0 if it has not reached)
        self.score = (int(parts[1].replace('goal=', ''))
                      if self.at_goal else 0)

        # is_done indicates whether the frog has finished the episode
        # (which can happen if the frog reaches the goal row or the
        # timer runs out)
        self.is_done = self.at_goal or (parts[1] == 'done')

    def is_legal(self, x, y):
        '''Returns true if x,y is a legal position in the game'''
        return x >= 0 and x < self.max_x and y >= 0 and y < self.max_y

    def get(self, x, y):
        '''Returns the game object (a single character) at x,y'''
        return (self.screen[y][x]
                if x >= 0 and x < self.max_x and y >= 0 and y < self.max_y
                else None)
