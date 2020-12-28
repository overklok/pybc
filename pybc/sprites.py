import pygame as pg

from pybc import (
    settings as sts
)


class Player(pg.sprite.Sprite):
    def __init__(self, grid):
        super().__init__()
        self.grid = grid

        self.surf = pg.Surface((self.grid.tilesize, self.grid.tilesize))
        self.surf.fill(sts.CL_YELLOW)

        self.rect = self.surf.get_rect()

        self.x = 0
        self.y = 0

        self.speed = 1

    def move(self, dx=0, dy=0):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def move_cell(self, dx=0, dy=0):
        x, y = self.grid.get_cell(self.x, self.y)

        self.x = x + dx * self.grid.tilesize
        self.y = y + dy * self.grid.tilesize

    def update(self):
        self.rect.x = self.grid.x_from + self.x
        self.rect.y = self.grid.y_from + self.y

class Wall(pg.sprite.Sprite):
    def __init__(self, grid, x, y):
        super().__init__()
        self.grid = grid

        self.surf = pg.Surface((self.grid.tilesize, self.grid.tilesize))
        self.surf.fill(sts.CL_GREEN)

        self.rect = self.surf.get_rect()

        self.x = x
        self.y = y

        self.rect.x = self.grid.x_from + x * self.grid.tilesize
        self.rect.y = self.grid.y_from + y * self.grid.tilesize
