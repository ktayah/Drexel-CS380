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

        # this simple key uses the 3 object characters above the frog
        # and combines them into a key string
        return ''.join([
            self.get(self.frog_x - 1, self.frog_y - 1) or '_',
            self.get(self.frog_x, self.frog_y - 1) or '_',
            self.get(self.frog_x + 1, self.frog_y - 1) or '_',
        ])

    def reward(self):
        '''Returns a reward value for the state.'''

        if self.at_goal:
            return self.score
        elif self.is_done:
            return -10
        else:
            return 0


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

        # Testing
        self.win_count = 0

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

        This is the main method that interacts with the game interface:
        given a state string, it should return the action to be taken
        by the agent.

        The initial implementation of this method is simply a random
        choice among the possible actions. You will need to augment
        the code to implement Q-learning within the agent.
        '''
        q_state = Q_State(state_string)
        key = q_state.key
        reward = q_state.reward()
        at_goal = q_state.at_goal

        epsilon = 1 # value used to figure out exploit/explore rate needed, higher initially, lower over time
        max_epsilon = 1 
        min_epsilon = 0.01
        epsilon_decay = 0.005
        alpha = 0.7 # learning rate
        discount_factor = 0.1

        action = None

        exploit_explore_rate = random.uniform(0, 1)
        if exploit_explore_rate > epsilon and key in self.q:
            # Exploit
            action = max(self.q[key], key = lambda a: self.q[key][a])
        else:
            # Explore
            action = random.choice(State.ACTIONS)
            epsilon -= epsilon_decay # reduce rate at which we explore over time
            if key not in self.q:
                # current state is not in q table, initialize it
                self.q[key] = dict.fromkeys(State.ACTIONS, 0)

        if self.p_key != None:
            q_value = ((1 - alpha) * self.q[self.p_key][self.p_action]
                + alpha * (self.p_reward + discount_factor 
                * (self.q[key][action] - self.q[self.p_key][self.p_action])))
            
            self.q[self.p_key][self.p_action] = q_value

        if at_goal:
            self.win_count += 1

        self.p_key = key # previous key
        self.p_action = action # previous action
        self.p_reward = reward # previous reward
        self.save()
        return action
