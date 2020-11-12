import datetime
import os
import random
import time

from . import arcade
from .frog import Frog
from .icon import get_icon
from .image import get_image_path
from .sprite import Sprite

SCREENS = {
    'easy': 'EEEEEEEEEEEEEEEE|~~~KLLLLLLLLLLLLM~|TTTTTTTT~~TTTTTTT~|LLLM~KLLLLLLLM~~KL|SSSSSSSSSSSSSSSSSS|-----D------------|------------A-----|----------------C-|SSSSSSSSSSSSSSSSSS',
    'medium': 'EEEEEEEEEEEEEEEE|~~~KLLLM~~~KLLLM~~|TT~~TTTT~~~TT~~~~~|LLM~~~~KLLLLM~~~KL|SSSSSSSSSSSSSSSSSS|-----DD--------DD-|--AAA-------AAA---|------C---------C-|SSSSSSSSSSSSSSSSSS',
    'hard': 'EEEEEEEEEEEEEEEE|~~~KLLM~~~~KLLM~~~|TT~~~TT~~~~TT~~~~~|LLM~~~~~KLLM~~~~KL|SSSSSSSSSSSSSSSSSS|---DDD---DDD--DDD--|-AA----AA----AA---|------C--C------C-|SSSSSSSSSSSSSSSSSS',
}


class Frogger(arcade.Window):

    WINDOW_PADDING = 24
    TIME_STEP = 0.25

    def __init__(self, screen):
        screen_string = SCREENS[screen] if screen in SCREENS else screen
        lines = screen_string.split('|')
        self.max_y = len(lines)
        self.max_x = len(lines[0])

        super().__init__(self.max_x * Sprite.SIZE,
                         self.max_y * Sprite.SIZE + self.WINDOW_PADDING,
                         'Frogger')

        self.background = arcade.load_texture(get_image_path('background.png'))

        random.seed(datetime.datetime.now())

        self.user_controlled = True

        self.steps = 0
        self.max_steps = None

        self.restart_y = None

        self.terrains = []
        for line in lines:
            c = line[0]
            icon = get_icon(c)
            self.terrains.append(icon.terrain if icon else c)

        self.sprites = arcade.SpriteList()
        for gy, line in enumerate(lines):
            for gx, c in enumerate(line):
                icon = get_icon(c)
                if icon:
                    sprite = Sprite(self, icon, gx, gy)
                    self.sprites.append(sprite)

        self.frogs = [Frog(self, None, self.TIME_STEP)]

    def add_agent(self, agent):
        if self.user_controlled:
            self.user_controlled = False
            self.frogs = []
        next_index = len(self.frogs)
        self.frogs.append(
            Frog(self, agent, self.TIME_STEP, index=next_index)
        )

    def is_legal(self, gx, gy):
        return gx >= 0 and gx < self.max_x and gy >= 0 and gy < self.max_y

    def get_terrain(self, gy):
        return self.terrains[gy]

    def encode(self, frog):
        screen = [[self.get_terrain(y)] * self.max_x
                 for y in range(self.max_y)]

        for sprite in self.sprites:
            gx, gy = sprite.gx, sprite.gy
            if self.is_legal(gx, gy):
                screen[gy][gx] = sprite.encoding

        for f in self.frogs:
            if f != frog:
                screen[f.gy][f.gx] = 'f'
        for f in self.frogs:
            if f == frog:
                screen[f.gy][f.gx] = 'F'

        screen_encoding = '|'.join([''.join(row) for row in screen])

        note = ('goal={}'.format(frog.goal_score())
                if frog.at_goal() else
                ('done' if frog.is_done() else ''))

        return '{}${}'.format(screen_encoding, note)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            self.background)

        texts = ['P{}   Score: {}   Timer: {:.1f}'.format(i+1, frog.score, frog.timer)
                 for i, frog in enumerate(self.frogs)]
        arcade.draw_text(texts[0], 10, self.height - 23,
                         arcade.color.GRANNY_SMITH_APPLE, 15, bold=True)
        if len(texts) > 1:
            arcade.draw_text(texts[1], self.width - 10, self.height - 23,
                             arcade.color.CAPRI, 15, bold=True, anchor_x='right')

        self.sprites.draw()
        for frog in self.frogs:
            if frog.is_done() and not frog.at_goal():
                frog.to_red()
            else:
                frog.to_green()
            frog.draw()

        # arcade.finish_render()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q or key == arcade.key.ESCAPE:
            arcade.close_window()
        if self.user_controlled:
            frog = self.frogs[0]
            if key == arcade.key.UP and frog.gy > 0:
                frog.set_next_action('u')
            elif key == arcade.key.DOWN and frog.gy < self.max_y - 1:
                frog.set_next_action('d')
            elif key == arcade.key.LEFT:
                frog.set_next_action('l')
            elif key == arcade.key.RIGHT:
                frog.set_next_action('r')

    def on_update(self, dt):
        if self.max_steps is not None:
            if self.steps >= self.max_steps:
                arcade.close_window()
        self.steps += 1
        for frog in self.frogs:
            frog.choose_action()
        for sprite in self.sprites:
            sprite.step()
        for frog in self.frogs:
            frog.step()

    def run(self, steps=None, speed='slow', restart=None):
        self.steps = 0
        self.max_steps = steps

        if speed == 'slow':
            self.set_update_rate(self.TIME_STEP)
        elif speed == 'fast':
            self.set_update_rate(.001)
        else:
            self.set_update_rate(speed)

        self.restart_y = restart
        if self.restart_y:
            for frog in self.frogs:
                frog.restart()

        arcade.run()

        return [frog.score for frog in self.frogs]
