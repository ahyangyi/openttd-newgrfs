import grf
from station.lib import AStation, ALayout, AGroundSprite, AParentSprite, LayoutSprite, Demo
from agrf.magic import Switch
from ..layouts import named_tiles, layouts
from .semitraversable import horizontal_layout, get_single_index

named_tiles.globalize()

my_demo = Demo(
    "4×4 traversable flexible station layout",
    [
        [corner_third_f.T, front_gate.T, front_gate.TR, corner_third_f.TR],
        [side_a3_n.T, central_windowed, central_windowed.R, side_a3_n.TR],
        [side_a3_n, central_windowed, central_windowed.R, side_a3_n.R],
        [corner_third_f, front_gate, front_gate.R, corner_third_f.R],
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


def get_back_index(l, r):
    return get_front_index(l, r).T


def get_left_index(t, d):
    if t + d == 2:
        return [corner, side_a2, corner.T][t]
    if t + d == 3:
        return [corner, side_a3, side_a3.T, corner.T][t]
    if t + d == 4:
        return [corner, side_a, side_b2, side_a.T, corner.T][t]
    a = [corner, side_a, side_b, side_c, side_b.T, side_a.T, corner.T]
    if t < d:
        return a[min(t, 3)]
    else:
        return a[-1 - min(d, 3)]


left_wall = Switch(
    ranges={
        t: Switch(
            ranges={d: get_left_index(t, d) for d in range(16)},
            default=side_c,
            code="var(0x41, shift=8, and=0x0000000f)",
        )
        for t in range(16)
    },
    default=side_c,
    code="var(0x41, shift=12, and=0x0000000f)",
)


def get_central_index(l, r):
    return horizontal_layout(
        l,
        r,
        v_central,
        Switch(
            ranges={
                0x11: side_a2_windowed,
                **{0x10 + x: side_a3_windowed for x in range(2, 16)},
                **{0x1 + 0x10 * x: side_a3_windowed.T for x in range(2, 16)},
            },
            default=side_d,
            code="var(0x41, shift=8, and=0x000000ff)",
        ),  # TODO: a3 or a2_windowed for threetile?
        left_wall,
        central,
        central_windowed,
        central_windowed_extender,
    )


def get_front_index(l, r):
    return horizontal_layout(
        l,
        r,
        v_end_gate_third_f,
        Switch(
            ranges={0x1: corner_gate_2_third_f},
            default=corner_gate_third_f,
            code="var(0x41, shift=8, and=0x0000000f) + var(0x41, shift=12, and=0x0000000f)",  # XXX Fragile code due to .T
        ),  # TODO: a3 or a2_windowed for threetile?
        corner_third_f,
        front_normal,
        front_gate,
        front_gate_extender,
    )


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

traversable_station = AStation(
    id=0x01,
    translation_name="FLEXIBLE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b00111100,
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