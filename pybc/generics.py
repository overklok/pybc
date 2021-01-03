import math

from . import (
    settings as sts,
    helpers as hlp
)


def points_generator(p_from, p_to, step):
    for p in range(p_from, p_to, step):
        yield p

    if not ((p_to - p_from) % step):
        yield p_to


def points_centered(p_from, p_to, step, amount):
    p_size = p_to - p_from
    p_req = step * amount

    p_diff = int((p_size - p_req) / 2)

    p_from = p_from + p_diff 
    p_to = p_to - p_diff

    return p_from, p_to

class Grid:
    dim_x = sts.GD_DIM_X
    dim_y = sts.GD_DIM_Y

    cells = []

    def __init__(self):
        self.tilesize = None
        self.x_from, self.x_to, self.x_points = None, None, None
        self.y_from, self.y_to, self.y_points = None, None, None

        self.recalc()
        self.loadmap()

    def width(self):
        return self.x_to - self.x_from

    def height(self):
        return self.y_to - self.y_from

    def loadmap(self):
        self.cells = [[0] * self.dim_y for _ in range(self.dim_x)]
        self.cells[2][2:6] = [1] * 4
        self.cells[6][2:6] = [1] * 4
        self.cells[3][2:6:4]  = [1]
        self.cells[4][2:6:4]  = [1]
        self.cells[5][2:7:4]  = [1, 1]

    def obstacles(self, scope_from=None, scope_dim=None):
        for (i, j), cell in self.all_cells(scope_from, scope_dim):
            if cell == 1:
                yield (i, j)

    def all_cells(self, scope_from=None, scope_dim=None):
        cells = self.cells

        x_from, y_from = 0, 0

        if scope_from and scope_dim:
            x_from, x_to = max(0, scope_from[0] - scope_dim[0]), min(self.dim_x, scope_from[0] + scope_dim[0])
            y_from, y_to = max(0, scope_from[1] - scope_dim[1]), min(self.dim_y, scope_from[1] + scope_dim[1])

            cells = (row[x_from:x_to+1] for row in self.cells[y_from:y_to+1])

        for j, row in enumerate(cells):
            for i, cell in enumerate(row):
                yield (x_from + i, y_from + j), cell


    def resize(self, dx, dy):
        self.dim_x = hlp.clamp(1, sts.CS_WIDTH - 2 * sts.CS_PADDING, self.dim_x + dx)
        self.dim_y = hlp.clamp(1, sts.CS_HEIGHT - 2 * sts.CS_PADDING, self.dim_y + dy)

        self.recalc()

    def recalc(self):
        self.tilesize = int(min(
            (sts.CS_WIDTH - 2 * sts.CS_PADDING) / self.dim_x, 
            (sts.CS_HEIGHT - 2 * sts.CS_PADDING) / self.dim_y, 
        ))

        x_from, x_to = sts.CS_PADDING, sts.CS_WIDTH - sts.CS_PADDING
        y_from, y_to = sts.CS_PADDING, sts.CS_HEIGHT - sts.CS_PADDING

        self.x_from, self.x_to = points_centered(x_from, x_to, self.tilesize, self.dim_x)
        self.y_from, self.y_to = points_centered(y_from, y_to, self.tilesize, self.dim_y)

        self.x_points = list(points_generator(self.x_from, self.x_to, self.tilesize))
        self.y_points = list(points_generator(self.y_from, self.y_to, self.tilesize))

    def intersects_with(self, cells, x, y, w=None, h=None):
        w = w or self.tilesize
        h = h or self.tilesize

        for (i, j) in cells:
            obs_x_from, obs_y_from = self.get_cell_position(i, j)

            obs_x_to = obs_x_from + self.tilesize
            obs_y_to = obs_y_from + self.tilesize

            col_right = max(0, (x + w) - obs_x_from)
            col_left = max(0, obs_x_to - x)
            col_top = max(0, (y + h) - obs_y_from)
            col_bottom = max(0, obs_y_to - y)

            if col_top and col_bottom and col_right and col_left:
                return obs_x_from, obs_x_to, obs_y_from, obs_y_to

        return None 

    def get_cell_index(self, x, y, centered=False):
        if centered:
            x += self.tilesize / 2
            y += self.tilesize / 2

        return 0 if x == 0 else math.floor(self.dim_x * x / (self.x_to - self.x_from)), \
               0 if y == 0 else math.floor(self.dim_y * y / (self.y_to - self.y_from))

    def get_cell_position(self, i, j):
        return self.tilesize * i, \
               self.tilesize * j

