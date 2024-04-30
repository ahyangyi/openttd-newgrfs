import grf
from station.lib import (
    AStation,
    ALayout,
    AParentSprite,
    LayoutSprite,
    Demo,
    StationTileSwitch,
    make_horizontal_switch,
    make_vertical_switch,
)
from agrf.magic import Switch
from ..layouts import named_tiles, layouts, flexible_entries
from .common import (
    horizontal_layout,
    make_cb14,
    get_central_index,
    determine_platform_odd,
    determine_platform_even,
    make_row,
    make_front_row,
)

named_tiles.globalize()

my_demos = [
    Demo(
        "4×4 semitraversable flexible station layout",
        [
            [corner_platform.T, front_gate.T, front_gate.T.R, corner_platform.T.R],
            [side_a3_n.T, central_windowed, central_windowed.R, side_a3_n.T.R],
            [side_a3_n, central_windowed, central_windowed.R, side_a3_n.R],
            [corner_platform, front_gate, front_gate.R, corner_platform.R],
        ],
    ),
    Demo(
        "4×4 semitraversable flexible station layout",
        [
            [corner.T, front_gate.T, front_gate.T.R, corner.T.R],
            [side_a3_f.T, central_windowed, central_windowed.R, side_a3_f.T.R],
            [side_a3_f, central_windowed, central_windowed.R, side_a3_f.R],
            [corner, front_gate, front_gate.R, corner.R],
        ],
    ),
]
demo_sprites = []
for demo in my_demos:
    for direction in [demo, demo.M]:
        demo_sprites.append(
            grf.AlternativeSprites(
                *[
                    LayoutSprite(direction, 64 * scale, 64 * scale, xofs=0, yofs=0, scale=scale, bpp=bpp)
                    for scale in [1, 2, 4]
                    for bpp in [32]
                ]
            )
        )
demo_layouts = [
    ALayout([], [AParentSprite(sprite, (16, 16, 48), (0, 0, 0))], False, category=b"\xe8\x8a\x9cA")
    for sprite in demo_sprites
]
layouts.extend(demo_layouts)
flexible_entries.extend([x for x in demo_layouts[::2]])


def get_front_index(l, r):
    return horizontal_layout(
        l,
        r,
        v_end_gate_platform,
        corner_gate_platform,
        corner_platform,
        front_normal_platform,
        front_gate_platform,
        front_gate_extender_platform,
    )


def get_front_index_2(l, r):
    return horizontal_layout(l, r, v_end_gate, corner_gate, corner, front_normal, front_gate, front_gate_extender)


cb14_0 = make_cb14(get_front_index, lambda l, r: get_central_index(l, r, determine_platform_odd), None).to_index(
    layouts
)
cb14_1 = make_cb14(get_front_index_2, lambda l, r: get_central_index(l, r, determine_platform_even), None).to_index(
    layouts
)

front = make_front_row("_platform")
front2 = make_front_row("")

cb24_0 = make_vertical_switch(
    lambda t, d: 0 if t == 0 or d == 0 else {"n": 2, "f": 4, "d": 6}[determine_platform_odd(t, d)], cb24=True
)
cb24_1 = make_vertical_switch(
    lambda t, d: 0 if t == 0 or d == 0 else {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True
)

h_n = make_horizontal_switch(lambda l, r: get_central_index(l, r, lambda t, d: "n"))
h_f = make_horizontal_switch(lambda l, r: get_central_index(l, r, lambda t, d: "f"))
h_d = make_horizontal_switch(lambda l, r: get_central_index(l, r, lambda t, d: "d"))

cb14_2 = make_vertical_switch(lambda t, d: (front2 if d == 0 else front2.T if t == 0 else h_n))
cb14_4 = make_vertical_switch(lambda t, d: (front if d == 0 else front.T if t == 0 else h_f))
cb14_6 = make_vertical_switch(lambda t, d: (front if d == 0 else front.T if t == 0 else h_d))

cb14 = StationTileSwitch("T", {2: cb14_2, 3: cb14_2, 4: cb14_4, 5: cb14_4, 6: cb14_6, 7: cb14_6})

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
        "select_sprite_layout": grf.DualCallback(default=cb14_0, purchase=layouts.index(demo_layouts[0])),
    },
)

semitraversable_station_no_side = AStation(
    id=0x01,
    translation_name="FLEXIBLE_UNTRAVERSABLE_NO_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b00111100,
    disabled_platforms=0b111,
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
        "select_sprite_layout": grf.DualCallback(default=cb14_1, purchase=layouts.index(demo_layouts[2])),
    },
)
