from . import arcade
from .image import get_image_path


class Icon:

    def __init__(self, name, x, y, encoding, dgx=0, terrain=None):
        self.name = name
        self.texture = arcade.load_texture(get_image_path('sprites.png'),
                                           x=x, y=y, width=48, height=48)
        self.encoding = encoding
        self.dgx = dgx
        self.terrain = terrain


ICONS = {
    '1': Icon('frog_green', 3, 3, 'F'),
    '2': Icon('frog_purple', 3, 57, 'F'),
    '3': Icon('frog_red', 3, 111, 'F'),
    'E': Icon('end', 309, 510, '+'),
    'S': Icon('safe', 407, 588, ' '),
    'K': Icon('log_left', 3, 402, '[', -1, '~'),
    'L': Icon('log_middle', 57, 402, '[', -1, '~'),
    'M': Icon('log_right', 111, 402, '[', -1, '~'),
    'T': Icon('turtle', 384, 456, ']', +1, '~'),
    'A': Icon('car_A', 3, 348, '<', -1, '-'),
    'B': Icon('car_B', 57, 348, '<', -1, '-'),
    'C': Icon('car_C', 111, 348, '>', +1, '-'),
    'D': Icon('car_D', 165, 348, '>', +1, '-'),
}


def get_icon(c):
    return ICONS[c] if c in ICONS else None
