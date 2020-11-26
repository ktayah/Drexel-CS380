import json
import os
import random

from .state import State


class Q_State(State):
    '''Augments the game state with Q-learning information'''

    def __init__(self, string):
        super().__init__(string)

        # key stores the state's key string (see notes in _compute_key())
        self.key = self._compute_key()

    def _compute_key(self):
        '''
        Returns a key used to index this state.

        The key should reduce the entire game state to something much smaller
        that can be used for learning. When implementing a Q table as a
        dictionary, this key is used for accessing the Q values for this
        state within the dictionary.
        '''

        # this simple key uses the 3 object characters above the frog and the two besides the frog, and the character +2 in the y direction
        # and combines them into a key string
        return ''.join([
            self.get(self.frog_x - 1, self.frog_y - 1) or '_',
            self.get(self.frog_x, self.frog_y - 1) or '_',
            self.get(self.frog_x, self.frog_y - 2) or '_',
            self.get(self.frog_x + 1, self.frog_y - 1) or '_',
            self.get(self.frog_x - 1, self.frog_y) or '_',
            self.get(self.frog_x + 1, self.frog_y) or '_',
        ])

    def reward(self):
        '''Returns a reward value for the state.'''
        if self.at_goal:
            return self.score
        elif self.is_done:
            return -1000
        else:
            return -1 * (self.frog_y + ((self.max_x + 1) // 2 % (self.frog_x + 1))) # closer to home row means higher reward


class Agent:

    def __init__(self, train=None):

        # train is either a string denoting the name of the saved
        # Q-table file, or None if running without training
        self.train = train

        # q is the dictionary representing the Q-table
        self.q = {}

        # name is the Q-table filename
        # (you likely don't need to use or change this)
        self.name = train or 'q'

        # the previously visited state key and previous action
        self.p_reward = None
        self.p_key = None
        self.p_action = None

        # some constants for exploit/explore rate evalulation
        # value used to figure out exploit/explore rate needed, higher initially, lower over time
        self.epsilon = 1
        self.epsilon_decay = 0.01
        self.min_epsilon = 0
        self.max_epsilon = 1

        # path is the path to the Q-table file
        # (you likely don't need to use or change this)
        self.path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'train', self.name + '.json')

        self.load()

    def load(self):
        '''Loads the Q-table from the JSON file'''
        try:
            with open(self.path, 'r') as f:
                self.q = json.load(f)
            if self.train:
                print('Training {}'.format(self.path))
            else:
                print('Loaded {}'.format(self.path))
        except IOError:
            if self.train:
                print('Training {}'.format(self.path))
            else:
                raise Exception('File does not exist: {}'.format(self.path))
        return self

    def save(self):
        '''Saves the Q-table to the JSON file'''
        with open(self.path, 'w') as f:
            json.dump(self.q, f)
        return self

    def choose_action(self, state_string):
        '''
        Returns the action to perform.
        '''
        q_state = Q_State(state_string)
        key = q_state._compute_key()
        reward = q_state.reward()

        alpha = 0.8 # learning rate
        discount_factor = 0.8

        action = None

        if self.train == None and key in self.q:
            action = max(self.q[key], key = lambda a: self.q[key][a])
        elif self.train == None: # Fallback
            action = random.choice(State.ACTIONS)
        else:
            exploit_explore_rate = random.uniform(self.min_epsilon, self.max_epsilon)
            if exploit_explore_rate > self.epsilon and key in self.q:
                # Exploit
                action = max(self.q[key], key = lambda a: self.q[key][a])
            else:
                # Explore
                action = random.choice(State.ACTIONS)
                self.epsilon -= self.epsilon_decay # reduce rate at which we explore over time
                if key not in self.q:
                    # current state is not in q table, initialize it
                    self.q[key] = dict.fromkeys(State.ACTIONS, 0)

            if self.p_key != None:
                q_value = ((1 - alpha) * self.q[self.p_key][self.p_action]
                    + alpha * (self.p_reward + (discount_factor 
                    * self.q[key][action]) - self.q[self.p_key][self.p_action]))
                self.q[self.p_key][self.p_action] = q_value

            self.p_key = key # previous key
            self.p_action = action # previous action
            self.p_reward = reward # previous reward
            self.save()

        return action
