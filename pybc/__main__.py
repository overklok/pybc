import sys
import pygame as pg

from pybc import (
    helpers as hlp,
    settings as sts, 
    #sprites
)


class Game:
    gd_dim_x = sts.GD_DIM_X
    gd_dim_y = sts.GD_DIM_Y

    def __init__(self):
        pg.init()
        pg.display.set_caption(sts.TITLE)
        pg.key.set_repeat(500, 100)

        self.screen = pg.display.set_mode((sts.CS_WIDTH, sts.CS_HEIGHT))
        self.clock = pg.time.Clock()

        self.load_data()

    def load_data(self):
        pass

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = pg.sprite.Group()

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
                if event.key == pg.K_LEFT:   self.gd_dim_x = max(self.gd_dim_x - 1, 1)
                if event.key == pg.K_RIGHT:  self.gd_dim_x = min(self.gd_dim_x + 1, sts.CS_WIDTH - sts.CS_PADDING * 2)
                if event.key == pg.K_UP:     self.gd_dim_y = max(self.gd_dim_y - 1, 1)
                if event.key == pg.K_DOWN:   self.gd_dim_y = min(self.gd_dim_y + 1, sts.CS_HEIGHT - sts.CS_PADDING * 2)
    
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(sts.CS_BGCOLOR)

        self.draw_grid()
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()

    def draw_grid(self):
        tilesize = min(
            (sts.CS_WIDTH - 2 * sts.CS_PADDING) / self.gd_dim_x, 
            (sts.CS_HEIGHT - 2 * sts.CS_PADDING) / self.gd_dim_y, 
        )

        tilesize = int(tilesize)

        x_from, x_to = sts.CS_PADDING, sts.CS_WIDTH - sts.CS_PADDING
        y_from, y_to = sts.CS_PADDING, sts.CS_HEIGHT - sts.CS_PADDING

        x_from, x_to, x_points = hlp.points_centered(x_from, x_to, tilesize, self.gd_dim_x)
        y_from, y_to, y_points = hlp.points_centered(y_from, y_to, tilesize, self.gd_dim_y)

        for x in x_points:
            pg.draw.line(self.screen, sts.CL_LIGHTGREY, (x, y_from), (x, y_to))

        for y in y_points:
            pg.draw.line(self.screen, sts.CL_LIGHTGREY, (x_from, y), (x_to, y))

g = Game()

while True:
    g.new()
    g.run()