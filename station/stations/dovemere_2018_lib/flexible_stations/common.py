import grf
from agrf.magic import Switch
from station.lib import make_horizontal_switch, make_vertical_switch, ALayout, AParentSprite, LayoutSprite, Demo
from ..layouts import named_tiles, layouts, flexible_entries


def make_demo(switch, w, h, preswitch=None):
    demo = Demo("", switch.demo(w, h, preswitch))
    for i, var in enumerate([var for var in [demo, demo.M]]):
        sprite = grf.AlternativeSprites(
            *[
                LayoutSprite(
                    var,
                    64 * scale,
                    64 * scale,
                    xofs=(1 - i % 2 * 2) * int((w - h) / (w + h + 1) * 32 * scale),
                    yofs=0,
                    scale=scale,
                    bpp=bpp,
                )
                for scale in [1, 2, 4]
                for bpp in [32]
            ]
        )
        layout = ALayout([], [AParentSprite(sprite, (16, 16, 48), (0, 0, 0))], False, category=b"\xe8\x8a\x9cA")
        layouts.append(layout)
        if i == 0:
            ret = layout
    flexible_entries.append(ret)
    return ret


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


def make_row(onetile, twotile, lwall, general, window, window_extender, threetile=None):
    return make_horizontal_switch(
        lambda l, r: horizontal_layout(
            l, r, onetile, twotile, lwall, general, window, window_extender, threetile=threetile
        )
    )


def make_front_row(suffix):
    return make_row(
        *[
            named_tiles[c + suffix]
            for c in ["v_end_gate", "corner_gate", "corner", "front_normal", "front_gate", "front_gate_extender"]
        ]
    )


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
    return make_vertical_switch(lambda t, d: get_left_index(d, t, cb))


def get_left_wall_2(cb):
    return make_vertical_switch(
        lambda t, d: (
            named_tiles.side_a2_windowed
            if (t, d) == (1, 1)
            else (
                get_tile("side_a3_windowed", cb(t, d))
                if d == 1
                else (get_tile("side_a3_windowed", cb(d, t)).T if t == 1 else get_tile_sym("side_d", cb(d, t)))
            )
        )
    )


def get_v_central(cb):
    return make_vertical_switch(lambda t, d: get_tile_sym("v_central", cb(t, d)))


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
    )


def get_left_index_suffix(t, d, suffix):
    if d > t:
        return get_left_index_suffix(d, t, suffix).T
    if t + d == 2:
        return named_tiles.side_a2
    if t + d == 3:
        return [get_tile("side_a3", suffix)][d - 1]
    if t + d == 4:
        return [get_tile("side_a", suffix), get_tile_sym("side_b2", suffix)][d - 1]
    if t == d:
        return named_tiles.side_c
    if d == 1:
        return get_tile("side_a", suffix)
    if d == 2:
        return get_tile("side_b", suffix)
    return get_tile_sym("side_c", suffix)


def make_central_row(l, r, suffix):
    return horizontal_layout(
        l,
        r,
        named_tiles.central,
        named_tiles.central,
        make_vertical_switch(lambda t, d: get_left_index_suffix(t, d, suffix)),
        named_tiles.central,
        named_tiles.central_windowed,
        named_tiles.central_windowed_extender,
    )


def determine_platform_odd(t, d):
    if d > t:
        return {"f": "n", "n": "f", "d": "d"}[determine_platform_odd(d, t)]
    if (t + d) % 2 == 1:
        return "fn"[d % 2]
    if (t + d) % 4 == 0:
        if d < t - 2:
            return "fn"[d % 2]
        return "d"
    if d < t:
        return "fn"[d % 2]
    return "d"


def determine_platform_even(t, d):
    if d > t:
        return {"f": "n", "n": "f", "d": "d"}[determine_platform_even(d, t)]
    if (t + d) % 2 == 1:
        return "nf"[d % 2]
    if (t + d) % 4 == 0:
        if d < t:
            return "nf"[d % 2]
        return "d"
    if d < t - 2:
        return "nf"[d % 2]
    return "d"
