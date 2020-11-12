import random

from . import arcade
from .icon import get_icon
from .sprite import Sprite


class Frog(Sprite):

    TIME_ALLOWED = 30.0

    def __init__(self, game, agent, time_step, index=0):
        super().__init__(game, get_icon(str(index+1)), 0, 0)
        self.agent = agent
        self.time_step = time_step
        self.frog_texture = self.texture
        self.red_texture = get_icon('3').texture
        self.score = 0
        self.timer = self.TIME_ALLOWED
        self.next_action = None
        self.restart_after_step = False
        self.restart()

    def collisions(self):
        hits = []
        for sprite in self.game.sprites:
            if sprite.dgx != 0 and arcade.check_for_collision(self, sprite):
                hits.append(sprite)
        return hits

    def is_done(self):
        terrain = self.game.get_terrain(self.gy)
        collisions = self.collisions()
        return (self.at_goal()
                or (self.timer <= 0)
                or (self.gx < 0 or self.gx >= self.game.max_x)
                or (terrain == '~' and not collisions)
                or (terrain == '-' and collisions))

    def at_goal(self):
        return self.gy == 0

    def goal_score(self):
        return (50 + int(20 * self.timer)
                if self.at_goal() else
                0)

    def to_red(self):
        self.texture = self.red_texture
        return self

    def to_green(self):
        self.texture = self.frog_texture
        return self

    ACTION_DELTAS = {'u': (0, -1), 'd': (0, +1),
                     'l': (-1, 0), 'r': (+1, 0), '_': (0, 0)}

    def set_next_action(self, action):
        self.next_action = action

    def choose_action(self):
        if self.is_done():
            if self.at_goal():
                self.score += self.goal_score()
            self.restart_after_step = True

        if self.agent:
            state = self.game.encode(self)
            self.next_action = self.agent.choose_action(state)

    def step(self):
        if ((not self.next_action or self.next_action not in 'ud')
                and self.game.get_terrain(self.gy) == '~'):
            floaters = [s for s in self.game.sprites if s.gy == self.gy]
            if floaters:
                self.move_by(floaters[0].dgx, 0)
        if self.next_action and not self.is_done():
            dx, dy = self.ACTION_DELTAS[self.next_action]
            self.move_by(dx, dy)

        self.next_action = None
        self.timer -= self.time_step

        if self.restart_after_step:
            self.restart()
            self.restart_after_step = False

    def restart(self):
        # print('restarting')
        self.timer = self.TIME_ALLOWED
        y = self.game.restart_y or (self.game.max_y - 1)
        self.move_to(random.randint(0, self.game.max_x - 1), y)
        while self.is_done():
            self.move_to(random.randint(0, self.game.max_x - 1), y)
