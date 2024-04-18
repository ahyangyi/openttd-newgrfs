import grf
from station.lib import AStation, ALayout, ADefaultGroundSprite, AParentSprite, LayoutSprite, Demo
from agrf.magic import Switch
from ..layouts import named_tiles, layouts, platform
from .semitraversable import horizontal_layout

named_tiles.globalize()

my_demo = Demo(
    "1×4 side station layout", [[h_end_asym_platform, h_gate_1_platform, h_gate_1_platform.R, h_end_asym_platform.R]]
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


def get_side_index(l, r):
    return horizontal_layout(l, r, tiny_asym_platform, h_end_asym_platform, h_normal, h_gate, h_gate_extender)


cb14 = Switch(
    ranges={
        l: Switch(
            ranges={r: get_side_index(l, r) for r in range(16)},
            default=h_normal,
            code="var(0x41, shift=0, and=0x0000000f)",
        )
        for l in range(16)
    },
    default=h_normal,
    code="var(0x41, shift=4, and=0x0000000f)",
)

side_station = AStation(
    id=0x02,
    translation_name="FLEXIBLE_FRONT_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b11,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(default=cb14.to_index(layouts), purchase=layouts.index(demo_layout1)),
    },
)

back_side_station = AStation(
    id=0x03,
    translation_name="FLEXIBLE_BACK_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b11,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(
            default=cb14.T.to_index(layouts), purchase=layouts.index(demo_layout1)
        ),
    },
)
