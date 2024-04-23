import grf
from station.lib import AStation, ALayout, AGroundSprite, AParentSprite, LayoutSprite, Demo
from agrf.magic import Switch
from ..layouts import named_tiles, layouts, flexible_entries
from .common import horizontal_layout, make_cb14, get_central_index, determine_platform_odd, determine_platform_even

named_tiles.globalize()

my_demos = [
    Demo(
        "4×4 traversable flexible station layout",
        [
            [corner_third_f.T, front_gate.T, front_gate.TR, corner_third_f.TR],
            [side_a3_n.T, central_windowed, central_windowed.R, side_a3_n.TR],
            [side_a3_n, central_windowed, central_windowed.R, side_a3_n.R],
            [corner_third_f, front_gate, front_gate.R, corner_third_f.R],
        ],
    ),
    Demo(
        "4×4 semitraversable flexible station layout",
        [
            [corner_third.T, front_gate.T, front_gate.TR, corner_third.TR],
            [side_a3_f.T, central_windowed, central_windowed.R, side_a3_f.TR],
            [side_a3_f, central_windowed, central_windowed.R, side_a3_f.R],
            [corner_third, front_gate, front_gate.R, corner_third.R],
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
    ALayout(
        AGroundSprite(grf.EMPTY_SPRITE),
        [AParentSprite(sprite, (16, 16, 48), (0, 0, 0))],
        False,
        category=b"\xe8\x8a\x9cA",
    )
    for sprite in demo_sprites
]
layouts.extend(demo_layouts)
flexible_entries.extend([x for x in demo_layouts[::2]])


def get_front_index(l, r):
    return horizontal_layout(
        l,
        r,
        v_end_gate_third_f,
        corner_gate_third_f,
        corner_third_f,
        front_normal_third_f,
        front_gate_third_f,
        front_gate_extender_third_f,
    )


def get_front_index_2(l, r):
    return horizontal_layout(
        l,
        r,
        v_end_gate_third,
        corner_gate_third,
        corner_third,
        front_normal_third,
        front_gate_third,
        front_gate_extender_third,
    )


cb14_0 = make_cb14(get_front_index, lambda l, r: get_central_index(l, r, determine_platform_odd), None).to_index(
    layouts
)
cb14_1 = make_cb14(get_front_index_2, lambda l, r: get_central_index(l, r, determine_platform_even), None).to_index(
    layouts
)

traversable_station = AStation(
    id=0x02,
    translation_name="FLEXIBLE_SIDE",
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
        "select_sprite_layout": grf.DualCallback(default=cb14_0, purchase=layouts.index(demo_layouts[0])),
    },
)

traversable_station_no_side = AStation(
    id=0x03,
    translation_name="FLEXIBLE_NO_SIDE",
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
        "select_sprite_layout": grf.DualCallback(default=cb14_1, purchase=layouts.index(demo_layouts[2])),
    },
)
