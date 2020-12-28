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

    def __init__(self):
        self.tilesize = None
        self.x_from, self.x_to, self.x_points = None, None, None
        self.y_from, self.y_to, self.y_points = None, None, None

        self.recalc()

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

    def get_cell(self, x, y):
        return (self.x_to - self.x_from) // x, \
               (self.y_to - self.y_from) // y