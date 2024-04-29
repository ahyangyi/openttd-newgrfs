import grf
from station.lib import AStation, ALayout, AParentSprite, LayoutSprite, Demo, StationTileSwitch, make_vertical_switch
from ..layouts import named_tiles, layouts, flexible_entries
from .common import (
    horizontal_layout,
    make_cb14,
    get_central_index,
    determine_platform_odd,
    determine_platform_even,
    make_demo,
)

named_tiles.globalize()


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


def get_single_index(l, r):
    return horizontal_layout(l, r, tiny, h_end_gate, h_end, h_normal, h_gate, h_gate_extender)


cb24_0 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_odd(t, d)], cb24=True)
cb24_1 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True)

cb14_2 = make_vertical_switch(
    lambda t, d: (
        make_horizontal_switch(get_front_index_2)
        if t == 0
        else make_horizontal_switch(get_front_index_2).T if d == 0 else get_central_index(t, d, lambda t, d: "n")
    )
)
cb14_4 = make_vertical_switch(
    lambda t, d: (
        make_horizontal_switch(get_front_index)
        if t == 0
        else make_horizontal_switch(get_front_index).T if d == 0 else get_central_index(t, d, lambda t, d: "f")
    )
)
cb14_6 = make_vertical_switch(
    lambda t, d: (
        make_horizontal_switch(get_front_index)
        if t == 0
        else make_horizontal_switch(get_front_index).T if d == 0 else get_central_index(t, d, lambda t, d: "d")
    )
)

cb14 = StationTileSwitch("T", {2: cb14_2, 3: cb14_2, 4: cb14_4, 5: cb14_4, 6: cb14_6, 7: cb14_6})
cb14_0 = make_cb14(
    get_front_index, lambda l, r: get_central_index(l, r, determine_platform_odd), get_single_index
).to_index(layouts)
cb14_1 = make_cb14(
    get_front_index_2, lambda l, r: get_central_index(l, r, determine_platform_even), get_single_index
).to_index(layouts)

traversable_station = AStation(
    id=0x02,
    translation_name="FLEXIBLE_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    disabled_platforms=0b1,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(default=cb14_0, purchase=layouts.index(make_demo(cb14, 4, 4, cb24_0))),
    },
)

traversable_station_no_side = AStation(
    id=0x03,
    translation_name="FLEXIBLE_NO_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    callbacks={
        "select_tile_layout": 0,
        "select_sprite_layout": grf.DualCallback(default=cb14_1, purchase=layouts.index(make_demo(cb14, 4, 4, cb24_0))),
    },
)
