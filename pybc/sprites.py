import pygame as pg

from pybc import (
    settings as sts,
    debug as dbg
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

        self.speed = 6

    def dmove(self, dx=0, dy=0):
        dx *= self.speed
        dy *= self.speed

        dx, dy = self.can_dmove(dx, dy)

        self.x += dx
        self.y += dy

    def dmove_cell(self, di=0, dj=0):
        i, j = self.grid.get_cell_index(self.x, self.y)

        self.x = i + di * self.grid.tilesize
        self.y = j + dj * self.grid.tilesize

    def can_dmove(self, dx=0, dy=0):
        x = self.x + dx
        y = self.y + dy

        ci, cj = self.grid.get_cell_index(x, y, centered=True)

        dbg.v_point_set(self.grid.x_from + x, self.grid.y_from + y)

        for (i, j) in self.grid.obstacles((ci, cj), (1, 1)):
            obs_x_from, obs_y_from = self.grid.get_cell_position(i, j)

            obs_x_to = obs_x_from + self.grid.tilesize
            obs_y_to = obs_y_from + self.grid.tilesize

            col_right = max(0, (x + self.grid.tilesize) - obs_x_from)
            col_left = max(0, obs_x_to - x)
            col_top = max(0, (y + self.grid.tilesize) - obs_y_from)
            col_bottom = max(0, obs_y_to - y)

            if col_top and col_bottom and col_right and col_left:
                if dx > 0: dx = dx - col_right
                if dx < 0: dx = dx + col_left
                if dy > 0: dy = dy - col_top
                if dy < 0: dy = dy + col_bottom

                return dx, dy

        return dx, dy

    def update(self):
        self.rect.x = self.grid.x_from + self.x
        self.rect.y = self.grid.y_from + self.y


class Wall(pg.sprite.Sprite):
    def __init__(self, grid, x, y, color=sts.CL_GREEN):
        super().__init__()

        self.grid = grid

        self.surf = pg.Surface((self.grid.tilesize, self.grid.tilesize))
        self.surf.fill(color)

        self.rect = self.surf.get_rect()

        self.x = x
        self.y = y

        self.rect.x = self.grid.x_from + x * self.grid.tilesize
        self.rect.y = self.grid.y_from + y * self.grid.tilesize

