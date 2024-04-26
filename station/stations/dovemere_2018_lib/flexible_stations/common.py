from agrf.magic import Switch
from ..layouts import named_tiles


def horizontal_layout(l, r, onetile, twotile, lwall, general, window, window_extender, threetile=None):
    threetile = threetile or twotile
    if l + r == 0:
        return onetile
    if l + r == 1:
        return [twotile, twotile.R][l]
    if l + r == 2:
        return [threetile, window_extender, threetile.R][l]

    e = l + r - 3
    c = (e + 1) // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return ([lwall] + [general] * o + [window] + [window_extender] * c + [window.R] + [general] * o + [lwall.R])[l]


def get_tile(name, desc):
    if desc == "f":
        return named_tiles[name + "_f"]
    if desc == "d":
        return named_tiles[name]
    return named_tiles[name + "_n"]


def get_tile_sym(name, desc):
    if desc == "f":
        return named_tiles[name + "_n"].T
    if desc == "d":
        return named_tiles[name]
    return named_tiles[name + "_n"]


def make_cb14(get_front_index, get_central_index, get_single_index):
    return Switch(
        ranges={
            **(
                {
                    (0, 1): Switch(
                        ranges={
                            l: Switch(
                                ranges={r: get_single_index(l, r) for r in range(16)},
                                default=named_tiles.tiny,
                                code="var(0x41, shift=0, and=0x0000000f)",
                            )
                            for l in range(16)
                        },
                        default=named_tiles.tiny,
                        code="var(0x41, shift=4, and=0x0000000f)",
                    )
                }
                if get_single_index is not None
                else {}
            ),
            (2, 3): Switch(
                ranges={
                    l: Switch(
                        ranges={r: get_front_index(l, r).T for r in range(16)},
                        default=named_tiles.tiny,
                        code="var(0x41, shift=0, and=0x0000000f)",
                    )
                    for l in range(16)
                },
                default=named_tiles.tiny,
                code="var(0x41, shift=4, and=0x0000000f)",
            ),
            (4, 5): Switch(
                ranges={
                    l: Switch(
                        ranges={r: get_front_index(l, r) for r in range(16)},
                        default=named_tiles.tiny,
                        code="var(0x41, shift=0, and=0x0000000f)",
                    )
                    for l in range(16)
                },
                default=named_tiles.tiny,
                code="var(0x41, shift=4, and=0x0000000f)",
            ),
            (6, 7): Switch(
                ranges={
                    l: Switch(
                        ranges={r: get_central_index(l, r) for r in range(16)},
                        default=named_tiles.tiny,
                        code="var(0x41, shift=0, and=0x0000000f)",
                    )
                    for l in range(16)
                },
                default=named_tiles.tiny,
                code="var(0x41, shift=4, and=0x0000000f)",
            ),
        },
        default=named_tiles.tiny,
        code="var(0x41, shift=24, and=0x0000000f)",
    )


def get_left_index(t, d, cb):
    if t > d:
        return get_left_index(d, t, cb).T
    if t + d == 2:
        return named_tiles.side_a2
    if t + d == 3:
        return [get_tile("side_a3", cb(1, 2))][t - 1]
    if t + d == 4:
        return [get_tile("side_a", cb(1, 3)), get_tile_sym("side_b2", cb(2, 2))][t - 1]
    if t == d:
        return named_tiles.side_c
    if t == 1:
        return get_tile("side_a", cb(t, d))
    if t == 2:
        return get_tile("side_b", cb(t, d))
    return get_tile_sym("side_c", cb(t, d))


def get_left_wall(cb):
    return Switch(
        ranges={
            t: Switch(
                ranges={d: get_left_index(t, d, cb) for d in range(1, 16)},
                default=named_tiles.side_c,
                code="var(0x41, shift=8, and=0x0000000f)",
            )
            for t in range(1, 16)
        },
        default=named_tiles.side_c,
        code="var(0x41, shift=12, and=0x0000000f)",
    )


def get_left_wall_2(cb):
    return Switch(
        ranges={
            t: Switch(
                ranges={
                    d: (
                        named_tiles.side_a2_windowed
                        if (t, d) == (1, 1)
                        else (
                            get_tile("side_a3_windowed", cb(t, d))
                            if t == 1
                            else (
                                get_tile("side_a3_windowed", cb(d, t)).T if d == 1 else get_tile_sym("side_d", cb(t, d))
                            )
                        )
                    )
                    for d in range(1, 16)
                },
                default=named_tiles.side_d,
                code="var(0x41, shift=8, and=0x0000000f)",
            )
            for t in range(1, 16)
        },
        default=named_tiles.side_d,
        code="var(0x41, shift=12, and=0x0000000f)",
    )


def get_v_central(cb):
    return Switch(
        ranges={
            t: Switch(
                ranges={d: get_tile_sym("v_central", cb(t, d)) for d in range(1, 16)},
                default=named_tiles.v_central,
                code="var(0x41, shift=8, and=0x0000000f)",
            )
            for t in range(1, 16)
        },
        default=named_tiles.v_central,
        code="var(0x41, shift=12, and=0x0000000f)",
    )


def get_central_index(l, r, cb):
    return horizontal_layout(
        l,
        r,
        get_v_central(cb),
        get_left_wall_2(cb),
        get_left_wall(cb),
        named_tiles.central,
        named_tiles.central_windowed,
        named_tiles.central_windowed_extender,
        # TODO: a3 or a2_windowed for threetile?
    )


def determine_platform_odd(t, d):
    if t > d:
        return {"f": "n", "n": "f", "d": "d"}[determine_platform_odd(d, t)]
    if (t + d) % 2 == 1:
        return "fn"[t % 2]
    if (t + d) % 4 == 0:
        if t < d - 2:
            return "fn"[t % 2]
        return "d"
    if t < d:
        return "fn"[t % 2]
    return "d"


def determine_platform_even(t, d):
    if t > d:
        return {"f": "n", "n": "f", "d": "d"}[determine_platform_even(d, t)]
    if (t + d) % 2 == 1:
        return "nf"[t % 2]
    if (t + d) % 4 == 0:
        if t < d:
            return "nf"[t % 2]
        return "d"
    if t < d - 2:
        return "nf"[t % 2]
    return "d"
