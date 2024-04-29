import grf
from station.lib import AStation, Demo, make_horizontal_switch
from agrf.magic import Switch
from ..layouts import named_tiles, layouts
from .semitraversable import horizontal_layout
from .common import make_demo

named_tiles.globalize()


def get_side_index(l, r):
    return horizontal_layout(
        l,
        r,
        tiny_asym_platform,
        h_end_asym_gate_platform,
        h_end_asym_platform,
        h_normal_platform,
        h_gate_1_platform,
        h_gate_extender_1_platform,
    )


def get_side_index_2(l, r):
    return horizontal_layout(l, r, tiny_asym, h_end_asym_gate, h_end_asym, h_normal, h_gate_1, h_gate_extender_1)


cb14 = make_horizontal_switch(get_side_index)
cb14_2 = make_horizontal_switch(get_side_index_2)


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
            default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 1))
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
            default=cb14.T.to_index(layouts), purchase=layouts.index(make_demo(cb14.T, 4, 1))
        ),
    },
)

side_station_np = AStation(
    id=0x06,
    translation_name="FLEXIBLE_FRONT_SIDE_NP",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b11,
    disabled_platforms=0b11111110,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(
            default=cb14_2.to_index(layouts), purchase=layouts.index(make_demo(cb14_2, 4, 1))
        ),
    },
)

back_side_station_np = AStation(
    id=0x07,
    translation_name="FLEXIBLE_BACK_SIDE_NP",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b11,
    disabled_platforms=0b11111110,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(
            default=cb14_2.T.to_index(layouts), purchase=layouts.index(make_demo(cb14_2.T, 4, 1))
        ),
    },
)
