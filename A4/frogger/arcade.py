from .settings import settings

if settings['use_graphics']:

    from arcade import *
    from arcade import color, key

else:

    import time

    _window = None

    class Sprite:
        pass

    class Window:

        def __init__(self, *args, **kwargs):
            self.update_rate = .001
            global _window
            _window = self

        def set_update_rate(self, rate):
            self.update_rate = rate

    class SpriteList:

        def __init__(self):
            self.sprites = []

        def __iter__(self):
            return iter(self.sprites)

        def append(self, sprite):
            self.sprites.append(sprite)

        def draw(self):
            pass

    def load_texture(*args, **kwargs):
        return None

    def check_for_collision(sprite1, sprite2):
        return sprite1.gx == sprite2.gx and sprite1.gy == sprite2.gy

    def close_window():
        global _window
        _window = None

    def run():
        if _window:
            game = _window
            frog = game.frogs[0]
            dt = _window.update_rate
            while _window:

                print()
                print(frog.score)
                screen = game.encode(frog).split('$')[0]
                screen = screen.replace('|', '\n')
                print(screen)
                print()

                _window.on_update(dt)

                time.sleep(dt)
