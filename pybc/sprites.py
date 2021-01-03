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

        self.vx, self.vy = 0, 0
        self.x, self.y = 0, 0

        self.speed = sts.PLAYER_SPEED

    def handle(self):
        self.vx, self.vy = 0, 0

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]  or keys[pg.K_a]: self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]: self.vx =  self.speed
        if keys[pg.K_UP]    or keys[pg.K_w]: self.vy = -self.speed
        if keys[pg.K_DOWN]  or keys[pg.K_s]: self.vy =  self.speed

        if self.vx != 0 and self.vy != 0:
            self.vx = 0.7071
            self.vy = 0.7071

    def update(self, dt):
        x, y = self.collide(dt * self.vx, dt * self.vy)

        self.x = x
        self.y = y

        self.rect.x = self.grid.x_from + self.x
        self.rect.y = self.grid.y_from + self.y

    def move_to_cell(self, di=0, dj=0):
        i, j = self.grid.get_cell_index(self.x, self.y)

        x, y = self.grid.get_cell_position(i + di, j + dj)

        dx = x - self.x
        dy = y - self.y

        self.dmove(dx, dy)

    def collide(self, dx=0, dy=0):
        x, y = self.x, self.y

        if dx:
            x = self.x + dx

            if x < 0:
                if dx < 0: x = 0

            gx = self.grid.width() - self.grid.tilesize

            if x > gx:
                if dx > 0: x = gx

            ci, cj = self.grid.get_cell_index(x, y, centered=True)
            obs = self.grid.intersects_with(x=x, y=y, cells=self.grid.obstacles((ci, cj), (1, 1)))

            if obs:
                obs_x_from, obs_x_to, _, _ = obs
                if dx > 0: x = obs_x_from - self.grid.tilesize
                if dx < 0: x = obs_x_to

        if dy:
            y = self.y + dy

            if y < 0:
                if dy < 0: y = 0

            gy = self.grid.height() - self.grid.tilesize

            if y > gy:
                if dy > 0: y = gy

            ci, cj = self.grid.get_cell_index(x, y, centered=True)
            obs = self.grid.intersects_with(x=x, y=y, cells=self.grid.obstacles((ci, cj), (1, 1)))

            if obs:
                _, _, obs_y_from, obs_y_to = obs
                if dy > 0: y = obs_y_from - self.grid.tilesize
                if dy < 0: y = obs_y_to

        return x, y

class Obstacle(pg.sprite.Sprite):
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

