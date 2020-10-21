import os
import random
import sys
import time

PRINT_IN_COLOR = True


def get_arg(index, default=None):
    '''Returns the command-line argument, or the default if not provided'''
    return sys.argv[index] if len(sys.argv) > index else default


def clear_screen():
    '''Clears the terminal screen'''
    os.system('cls' if os.name == 'nt' else 'clear')


COLORS = ['black', 'red', 'green', 'yellow',
          'blue', 'purple', 'cyan', 'white']

COLOR_CODES = {c: i for i, c in enumerate(COLORS)}
STYLE_CODES = {None: 0, 'b': 1, 'u': 2}


def color_string(s, fore='black', back='white', style=None, index=None):
    '''Returns a new string colored as specified'''
    if PRINT_IN_COLOR:
        code = '\033[{};3{};4{}m'.format(
            STYLE_CODES[None if index else style],
            COLOR_CODES['white' if index else fore],
            index if index else COLOR_CODES[back])
        return code + s + '\033[0m'
    else:
        return s


def pprint(objs, sep=' ', per_row=12, indent=0, sort=False):
    '''Pretty-prints an object or list of objects, using pprint_string() if available'''
    if not isinstance(objs, list):
        objs = [objs]
    objs = [o.pprint_string() if getattr(o, 'pprint_string', None) else str(o)
            for o in objs]
    if sort:
        objs.sort()
    if len(objs) > per_row:
        pprint(objs[0:per_row], indent=indent)
        pprint(objs[per_row:], indent=4)
    elif len(objs) > 0:
        print()
        space = indent * ' '
        blocks = [s.split('\n') for s in objs]
        for i in range(len(blocks[0])):
            print(space + sep.join([b[i] for b in blocks]))
        print()
