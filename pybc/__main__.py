import sys
import pygame as pg

from pybc import (
    generics as gnr,
    settings as sts, 
    sprites as spr,
    debug as dbg,
)


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(sts.TITLE)
        pg.key.set_repeat(500, 100)

        self.dt = 0

        self.screen = pg.display.set_mode((sts.CS_WIDTH, sts.CS_HEIGHT))
        self.clock = pg.time.Clock()
        self.grid = gnr.Grid()

        self.sprites_all = pg.sprite.Group()
        self.sprites_obstacles = pg.sprite.Group()

        self.surf_dbg = pg.Surface((5, 5))
        self.surf_dbg.fill(sts.CL_RED)

        self.load_data()

    def load_data(self):
        pass

    def new(self):
        self.sprites_all = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = spr.Player(self.grid)

        for (x, y) in self.grid.obstacles():
            obstacle = spr.Obstacle(self.grid, x, y)

            self.sprites_obstacles.add(obstacle)
            self.sprites_all.add(obstacle)

        self.sprites_all.add(self.player)

    def run(self):
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(sts.FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: self.quit()

            self.player.handle()

    def update(self):
        self.sprites_all.update(self.dt)

    def draw(self):
        self.screen.fill(sts.CS_BGCOLOR)

        self.draw_grid()
        self.draw_sprites()
        self.draw_debug()

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()

    def draw_sprites(self):
        for entity in self.sprites_all:
            self.screen.blit(entity.surf, entity.rect)

    def draw_grid(self):
        for x in self.grid.x_points:
            pg.draw.line(self.screen, sts.CL_LIGHTGREY, (x, self.grid.y_from), (x, self.grid.y_to))

        for y in self.grid.y_points:
            pg.draw.line(self.screen, sts.CL_LIGHTGREY, (self.grid.x_from, y), (self.grid.x_to, y))

    def draw_debug(self):
        point = dbg.v_point_get()

        if point is not None:
            self.screen.blit(self.surf_dbg, point)

g = Game()

while True:
    g.new()
    g.run()
