import grf
from station.lib import AStation, ALayout, AGroundSprite, AParentSprite, LayoutSprite, Demo
from agrf.magic import Switch
from ..layouts import named_tiles, layouts
from .common import horizontal_layout

named_tiles.globalize()

my_demo = Demo(
    "4×4 semitraversable flexible station layout",
    [
        [corner_platform.T, front_gate.T, front_gate.TR, corner_platform.TR],
        [side_a3_n.T, central_windowed, central_windowed.R, side_a3_n.TR],
        [side_a3_n, central_windowed, central_windowed.R, side_a3_n.R],
        [corner_platform, front_gate, front_gate.R, corner_platform.R],
    ],
)
demo_sprites = []
for demo in [my_demo, my_demo.M]:
    demo_sprites.append(
        grf.AlternativeSprites(
            *[
                LayoutSprite(demo, 64 * scale, 64 * scale, xofs=0, yofs=0, scale=scale, bpp=bpp)
                for scale in [1, 2, 4]
                for bpp in [32]
            ]
        )
    )
demo_layout1 = ALayout(
    AGroundSprite(grf.EMPTY_SPRITE), [AParentSprite(demo_sprites[0], (16, 16, 48), (0, 0, 0))], False
)
demo_layout2 = ALayout(
    AGroundSprite(grf.EMPTY_SPRITE), [AParentSprite(demo_sprites[1], (16, 16, 48), (0, 0, 0))], False
)
layouts.append(demo_layout1)
layouts.append(demo_layout2)


def determine_platform(t, d):
    if (t + d) % 2 == 1:
        return "fn"[t % 2]
    if (t + d) % 4 == 0:
        if t == 0 or d == 0:
            return "x"
        if t < d:
            return "nf"[t % 2]
        if t == d:
            return "d"
        return "fn"[t % 2]
    if t < d:
        return "fn"[t % 2]
    if t == d:
        return "d"
    return "nf"[t % 2]


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


smart_corner = Switch(
    ranges={d: corner for d in range(4, 16, 4)}, default=corner_platform, code="var(0x41, shift=8, and=0x000000ff)"
)
smart_corner_T = Switch(
    ranges={t * 0x10: corner.T for t in range(4, 16, 4)},
    default=corner_platform.T,
    code="var(0x41, shift=8, and=0x000000ff)",
)


def get_left_index(t, d, cb):
    if t > d:
        return get_left_index(d, t, cb).T
    if t + d == 2:
        return [side_a2][t - 1]
    if t + d == 3:
        return [get_tile("side_a3", cb(1, 2))][t - 1]
    if t + d == 4:
        return [get_tile("side_a", cb(1, 3)), get_tile_sym("side_b2", cb(2, 2))][t - 1]
    if t == d:
        return side_c
    if t == 1:
        return get_tile("side_a", cb(t, d))
    if t == 2:
        return get_tile("side_b", cb(t, d))
    return get_tile_sym("side_c", cb(t, d))


left_wall = Switch(
    ranges={
        t: Switch(
            ranges={d: get_left_index(t, d, determine_platform) for d in range(1, 16)},
            default=side_c,
            code="var(0x41, shift=8, and=0x0000000f)",
        )
        for t in range(1, 16)
    },
    default=side_c,
    code="var(0x41, shift=12, and=0x0000000f)",
)

left_wall_2 = Switch(
    ranges={
        t: Switch(
            ranges={
                d: (
                    side_a2_windowed
                    if (t, d) == (1, 1)
                    else (
                        get_tile("side_a3_windowed", determine_platform(t, d))
                        if t == 1
                        else (
                            get_tile("side_a3_windowed", determine_platform(d, t)).T
                            if d == 1
                            else get_tile_sym("side_d", determine_platform(t, d))
                        )
                    )
                )
                for d in range(1, 16)
            },
            default=side_d,
            code="var(0x41, shift=8, and=0x0000000f)",
        )
        for t in range(1, 16)
    },
    default=side_d,
    code="var(0x41, shift=12, and=0x0000000f)",
)


def get_central_index(l, r):
    return horizontal_layout(
        l,
        r,
        v_central,
        left_wall_2,
        left_wall,
        central,
        central_windowed,
        central_windowed_extender,
        # TODO: a3 or a2_windowed for threetile?
    )


def get_back_index(l, r):
    return horizontal_layout(
        l, r, v_end_gate.T, corner_gate.T, smart_corner_T, front_normal.T, front_gate.T, front_gate_extender.T
    )


def get_front_index(l, r):
    return horizontal_layout(l, r, v_end_gate, corner_gate, smart_corner, front_normal, front_gate, front_gate_extender)


def get_single_index(l, r):
    return horizontal_layout(l, r, tiny, h_end_gate, h_end, h_normal, h_gate, h_gate_extender)


cb14 = Switch(
    ranges={
        (0, 1): Switch(
            ranges={
                l: Switch(
                    ranges={r: get_single_index(l, r) for r in range(16)},
                    default=h_normal,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=h_normal,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
        (2, 3): Switch(
            ranges={
                l: Switch(
                    ranges={r: get_back_index(l, r) for r in range(16)},
                    default=front_normal.T,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=front_normal.T,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
        (4, 5): Switch(
            ranges={
                l: Switch(
                    ranges={r: get_front_index(l, r) for r in range(16)},
                    default=front_normal,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=front_normal,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
        (6, 7): Switch(
            ranges={
                l: Switch(
                    ranges={r: get_central_index(l, r) for r in range(16)},
                    default=central,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=central,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
    },
    default=central,
    code="var(0x41, shift=24, and=0x0000000f)",
).to_index(layouts)

semitraversable_station = AStation(
    id=0x00,
    translation_name="FLEXIBLE_UNTRAVERSABLE_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b00111100,
    disabled_platforms=0b11,
    callbacks={
        "select_tile_layout": grf.PurchaseCallback(
            purchase=Switch(
                ranges={
                    (2, 15): Switch(
                        ranges={0: 2},
                        default=Switch(ranges={0: 4}, default=6, code="(extra_callback_info1 >> 12) & 0xf"),
                        code="(extra_callback_info1 >> 8) & 0xf",
                    )
                },
                default=0,
                code="(extra_callback_info1 >> 20) & 0xf",
            )
        ),
        "select_sprite_layout": grf.DualCallback(default=cb14, purchase=layouts.index(demo_layout1)),
    },
)
