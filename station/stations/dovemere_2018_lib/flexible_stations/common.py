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
