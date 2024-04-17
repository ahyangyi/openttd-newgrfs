import grf
from station.lib import AStation, ALayout, ADefaultGroundSprite, AParentSprite, LayoutSprite, Demo
from agrf.magic import Switch
from ..layouts import named_tiles, layouts
from .semi_auto import horizontal_layout, get_single_index, get_central_index

named_tiles.globalize()

my_demo = Demo(
    "4×4 full station layout",
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
demo_layout1 = ALayout(ADefaultGroundSprite(1012), [AParentSprite(demo_sprites[0], (16, 16, 48), (0, 0, 0))], False)
demo_layout2 = ALayout(ADefaultGroundSprite(1011), [AParentSprite(demo_sprites[1], (16, 16, 48), (0, 0, 0))], False)
layouts.append(demo_layout1)
layouts.append(demo_layout2)


def get_back_index(l, r):
    return get_front_index(l, r).T


def get_front_index(l, r):
    return horizontal_layout(l, r, v_end_third_f, corner_third_f, front_normal, front_gate, front_gate_extender)


cb14_1 = Switch(
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

flex1 = AStation(
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
        "select_sprite_layout": grf.DualCallback(default=cb14_1, purchase=layouts.index(demo_layout1)),
    },
)
