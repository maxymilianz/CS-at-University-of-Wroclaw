from collections import deque


def is_legal(setting):
    b_king, w_king, w_rook = setting
    return w_king != w_rook != b_king and (abs(b_king[0] - w_king[0]) > 1 or abs(b_king[1] - w_king[1]) > 1) and \
           all(p[0] in range(8) and p[1] in range(8) for p in {b_king, w_king, w_rook})


def between(mid, pos_0, pos_1):
    mid_x, mid_y = mid
    x_0, y_0 = pos_0
    x_1, y_1 = pos_1
    return (mid_y == y_0 == y_1 and mid_x in range(min(x_0, x_1) + 1, max(x_0, x_1))) or \
           (mid_x == x_0 == x_1 and mid_y in range(min(y_0, y_1) + 1, max(y_0, y_1)))


def is_check(setting):
    b_king, w_king, w_rook = setting
    return (w_rook[0] == b_king[0] or w_rook[1] == b_king[1]) and not between(w_king, b_king, w_rook)


def moves(active_black, setting):
    b_king, w_king, w_rook = setting

    if active_black:
        k_x, k_y = b_king
        options = {(k_x-1, k_y-1), (k_x-1, k_y), (k_x-1, k_y+1), (k_x, k_y-1), (k_x, k_y+1), (k_x+1, k_y-1), (k_x+1, k_y), (k_x+1, k_y+1)}
        return {(option, w_king, w_rook) for option in options if is_legal((option, w_king, w_rook)) and not is_check((option, w_king, w_rook))}
    else:
        k_x, k_y = w_king
        r_x, r_y = w_rook

        k_options = {(k_x-1, k_y-1), (k_x-1, k_y), (k_x-1, k_y+1), (k_x, k_y-1), (k_x, k_y+1), (k_x+1, k_y-1), (k_x+1, k_y), (k_x+1, k_y+1)}
        r_options = {(x, r_y) for x in range(8) if x != r_x and not (between(b_king, w_rook, (x, r_y)) or between(w_king, w_rook, (x, r_y)))} | \
                    {(r_x, y) for y in range(8) if y != r_y and not (between(b_king, w_rook, (r_x, y)) or between(w_king, w_rook, (r_x, y)))}
                    
        return {(b_king, option, w_rook) for option in k_options if is_legal((b_king, option, w_rook))} | \
               {(b_king, w_king, option) for option in r_options if is_legal((b_king, w_king, option))}


def is_checkmate(setting):
    b_king, _, w_rook = setting
    return all(is_check(setting) for setting in moves(True, setting) | {tuple(setting)}) and (abs(b_king[0] - w_rook[0]) > 1 or abs(b_king[1] - w_rook[1]) > 1)


def closest_checkmate(active_black, start_setting):
    options = deque()
    options.appendleft((active_black, start_setting, []))
    used_options = set()

    while True:
        active_black, setting, used_settings = options.pop()
        new_used_settings = used_settings + [setting]

        if is_checkmate(setting):
            return new_used_settings

        new_active_black = not active_black

        for option in [(new_active_black, new_setting, new_used_settings) for new_setting in moves(active_black, setting)
                        if (new_active_black, new_setting) not in used_options]:
            options.appendleft(option)
            new_active_black, new_setting, new_used_settings = option
            used_options |= {(new_active_black, new_setting)}


def pos_to_coords(pos):
    return ord(pos[0]) - ord('a'), int(pos[1]) - 1


def coords_to_pos(coords):
    return chr(ord('a') + coords[0]) + str(coords[1] + 1)


def test(active_black, setting):
    path = closest_checkmate(active_black, tuple(pos_to_coords(pos) for pos in setting))
    return [[coords_to_pos(coords) for coords in step] for step in path]