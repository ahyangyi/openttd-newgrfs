import grf
from station.lib import make_horizontal_switch, make_vertical_switch, ALayout, AParentSprite, LayoutSprite, Demo
from ..layouts import named_tiles, layouts, flexible_entries


def make_demo(switch, w, h, preswitch=None):
    demo = Demo(switch.demo(w, h, preswitch))
    for i, var in enumerate([demo, demo.M]):
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
        layout = ALayout(None, [AParentSprite(sprite, (16, 16, 48), (0, 0, 0))], False, category=b"\xe8\x8a\x9cA")
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


def make_front_row(suffix, fallback_suffix=None):
    row = [
        named_tiles[(c, *suffix)] if (c, *suffix) in named_tiles else named_tiles[(c, *fallback_suffix)]
        for c in ["v_end_gate", "corner_gate", "corner", "front_normal", "front_gate", "front_gate_extender"]
    ]
    row[1] = make_vertical_switch(lambda t, d: named_tiles[("corner_gate_2", *suffix)] if t == 1 else row[1])
    row[2] = make_vertical_switch(lambda t, d: named_tiles[("corner_2", *suffix)] if t == 1 else row[2])
    return make_row(*row)


def get_tile(name, desc, fallback_suffix=None):
    # FIXME Remove fallback
    return named_tiles[(name, *desc)]


def reverse(x):
    if x is None:
        return None
    return x[:-1] + ({"f": "n", "n": "f", "d": "d"}[x[-1]],)


def get_left_index_suffix(t, d, suffix, fallback_suffix=None):
    if d > t:
        return get_left_index_suffix(d, t, reverse(suffix), reverse(fallback_suffix)).T
    if t + d == 2:
        return get_tile("side_a2", suffix, fallback_suffix)
    if t + d == 3:
        return get_tile("side_a3", suffix, fallback_suffix)
    if t + d == 4:
        return [get_tile("side_a", suffix, fallback_suffix), get_tile("side_b2", suffix, fallback_suffix)][d - 1]
    if t == d:
        return get_tile("side_c", suffix, fallback_suffix)
    if d == 1:
        return get_tile("side_a", suffix, fallback_suffix)
    if d == 2:
        return get_tile("side_b", suffix, fallback_suffix)
    return get_tile("side_c", suffix, fallback_suffix)


def get_left_index_suffix_2(t, d, suffix, fallback_suffix):
    if t == d == 1:
        return get_tile("side_a2_windowed", suffix, fallback_suffix)
    if d == 1:
        return get_tile("side_a3_windowed", suffix, fallback_suffix)
    if t == 1:
        return get_tile("side_a3_windowed", reverse(suffix), reverse(fallback_suffix)).T
    return get_tile("side_d", suffix, fallback_suffix)


def make_central_row(l, r, suffix, fallback_suffix=None):
    return horizontal_layout(
        l,
        r,
        make_vertical_switch(lambda t, d: get_tile("v_central", suffix, fallback_suffix)),
        make_vertical_switch(lambda t, d: get_left_index_suffix_2(t, d, suffix, fallback_suffix)),
        make_vertical_switch(lambda t, d: get_left_index_suffix(t, d, suffix, fallback_suffix)),
        make_vertical_switch(lambda t, d: get_tile("central", suffix, fallback_suffix)),
        make_vertical_switch(lambda t, d: get_tile("central_windowed", suffix, fallback_suffix)),
        make_vertical_switch(lambda t, d: get_tile("central_windowed_extender", suffix, fallback_suffix)),
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
