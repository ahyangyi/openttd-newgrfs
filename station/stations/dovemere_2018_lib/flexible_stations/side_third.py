import grf
from station.lib import AStation, make_horizontal_switch
from ..layouts import named_tiles, layouts
from .common import make_demo, horizontal_layout

named_tiles.globalize()


def get_side_index(l, r):
    return horizontal_layout(
        l,
        r,
        tiny_asym_third_f,
        h_end_asym_gate_third_f,
        h_end_asym_third_f,
        h_normal_third_f,
        h_gate_1_third_f,
        h_gate_extender_1_third_f,
    )


def get_side_index_2(l, r):
    return horizontal_layout(
        l,
        r,
        tiny_asym_third,
        h_end_asym_gate_third,
        h_end_asym_third,
        h_normal_third,
        h_gate_1_third,
        h_gate_extender_1_third,
    )


cb14 = make_horizontal_switch(get_side_index)
cb14_2 = make_horizontal_switch(get_side_index_2)

side_third_station = AStation(
    id=0x0E,
    translation_name="FLEXIBLE_FRONT_SIDE_THIRD",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    disabled_platforms=0b11111110,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(
            default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 1))
        ),
    },
)

back_side_third_station = AStation(
    id=0x0F,
    translation_name="FLEXIBLE_BACK_SIDE_THIRD",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    disabled_platforms=0b11111110,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(
            default=cb14.T.to_index(layouts), purchase=layouts.index(make_demo(cb14.T, 4, 1))
        ),
    },
)

side_third_station_np = AStation(
    id=0x10,
    translation_name="FLEXIBLE_FRONT_SIDE_THIRD_NP",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    disabled_platforms=0b11111110,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(
            default=cb14_2.to_index(layouts), purchase=layouts.index(make_demo(cb14_2, 4, 1))
        ),
    },
)

back_side_third_station_np = AStation(
    id=0x11,
    translation_name="FLEXIBLE_BACK_SIDE_THIRD_NP",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    disabled_platforms=0b11111110,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(
            default=cb14_2.T.to_index(layouts), purchase=layouts.index(make_demo(cb14_2.T, 4, 1))
        ),
    },
)
