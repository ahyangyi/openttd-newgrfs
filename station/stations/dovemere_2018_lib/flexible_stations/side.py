import grf
from station.lib import AStation, ALayout, AGroundSprite, AParentSprite, LayoutSprite, Demo
from agrf.magic import Switch
from ..layouts import named_tiles, layouts, flexible_entries
from .semitraversable import horizontal_layout

named_tiles.globalize()

my_demo = Demo(
    "1×4 side station layout", [[h_end_asym_platform, h_gate_1_platform, h_gate_1_platform.R, h_end_asym_platform.R]]
)
demo_layouts = []
for i, demo in enumerate([my_demo, my_demo.M, my_demo.T, my_demo.T.M]):
    sprite = grf.AlternativeSprites(
        *[
            LayoutSprite(demo, 64 * scale, 64 * scale, xofs=(16 - i % 2 * 32) * scale, yofs=0, scale=scale, bpp=bpp)
            for scale in [1, 2, 4]
            for bpp in [32]
        ]
    )
    layout = ALayout([], [AParentSprite(sprite, (16, 16, 48), (0, 0, 0))], False, category=b"\xe8\x8a\x9cA")
    demo_layouts.append(layout)
layouts.extend(demo_layouts)
flexible_entries.extend([x for x in demo_layouts[::2]])


def get_side_index(l, r):
    return horizontal_layout(
        l,
        r,
        tiny_asym_platform,
        h_end_asym_gate_platform,
        h_end_asym_platform,
        h_normal,  # FIXME need a platform version
        h_gate_1_platform,
        h_gate_extender_1_platform,
    )


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
    id=0x04,
    translation_name="FLEXIBLE_FRONT_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b11,
    disabled_platforms=0b11111110,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(
            default=cb14.to_index(layouts), purchase=layouts.index(demo_layouts[0])
        ),
    },
)

back_side_station = AStation(
    id=0x05,
    translation_name="FLEXIBLE_BACK_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b11,
    disabled_platforms=0b11111110,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(
            default=cb14.T.to_index(layouts), purchase=layouts.index(demo_layouts[2])
        ),
    },
)
