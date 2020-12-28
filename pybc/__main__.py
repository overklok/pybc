import sys
import pygame as pg

from pybc import (
    generics as gnr,
    settings as sts, 
    sprites as spr
)


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(sts.TITLE)
        pg.key.set_repeat(1, 0)

        self.screen = pg.display.set_mode((sts.CS_WIDTH, sts.CS_HEIGHT))
        self.clock = pg.time.Clock()
        self.grid = gnr.Grid()

        self.load_data()

    def load_data(self):
        pass

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = spr.Player(self.grid)

        self.all_sprites.add(self.player)

        for x in range(10, 20):
            wall = spr.Wall(self.grid, x, 5)
            self.all_sprites.add(wall)

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
                if event.key == pg.K_LEFT:   self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:  self.player.move(dx=1)
                if event.key == pg.K_UP:     self.player.move(dy=-1)
                if event.key == pg.K_DOWN:   self.player.move(dy=1)
    
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(sts.CS_BGCOLOR)

        self.draw_grid()
        self.draw_sprites()

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()

    def draw_sprites(self):
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

    def draw_grid(self):
        for x in self.grid.x_points:
            pg.draw.line(self.screen, sts.CL_LIGHTGREY, (x, self.grid.y_from), (x, self.grid.y_to))

        for y in self.grid.y_points:
            pg.draw.line(self.screen, sts.CL_LIGHTGREY, (self.grid.x_from, y), (self.grid.x_to, y))

g = Game()

while True:
    g.new()
    g.run()