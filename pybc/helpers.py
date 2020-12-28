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

    return p_from, p_to, points_generator(p_from, p_to, step)