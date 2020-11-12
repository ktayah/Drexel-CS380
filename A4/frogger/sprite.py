from . import arcade


class Sprite(arcade.Sprite):

    SIZE = 48

    def __init__(self, game, icon, gx, gy):
        super().__init__()
        self.game = game
        self.gx = gx
        self.gy = gy
        self.texture = icon.texture
        self.encoding = icon.encoding
        self.dgx = icon.dgx
        self.redraw()

    def redraw(self):
        self.center_x = self.SIZE * self.gx + 24
        self.center_y = self.SIZE * (self.game.max_y - self.gy) - 24
        return self

    def step(self):
        self.gx += self.dgx
        if self.gx > self.game.max_x:
            self.gx = -1
        elif self.gx < -1:
            self.gx = self.game.max_x
        return self.redraw()

    def move_to(self, gx, gy):
        if self.game.is_legal(gx, gy):
            self.gx = gx
            self.gy = gy
        return self.redraw()

    def move_by(self, dgx, dgy):
        if self.game.is_legal(self.gx + dgx, self.gy + dgy):
            self.gx += dgx
            self.gy += dgy
        return self.redraw()
