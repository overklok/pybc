V_POINT = None

def v_point_set(x=None, y=0):
    global V_POINT

    if x is None:
        V_POINT = None

    V_POINT = (x, y)


def v_point_get():
    global V_POINT

    return V_POINT
