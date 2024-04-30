import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch, make_horizontal_switch
from ..layouts import named_tiles, layouts
from .common import get_central_index, determine_platform_odd, determine_platform_even, make_demo, make_row

named_tiles.globalize()


front = make_row(
    v_end_gate_third_f,
    corner_gate_third_f,
    corner_third_f,
    front_normal_third_f,
    front_gate_third_f,
    front_gate_extender_third_f,
)


front2 = make_row(
    v_end_gate_third, corner_gate_third, corner_third, front_normal_third, front_gate_third, front_gate_extender_third
)


single = make_row(tiny, h_end_gate, h_end, h_normal, h_gate, h_gate_extender)


cb24_0 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_odd(t, d)], cb24=True)
cb24_1 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True)

h_n = make_horizontal_switch(lambda l, r: get_central_index(l, r, lambda t, d: "n"))
h_f = make_horizontal_switch(lambda l, r: get_central_index(l, r, lambda t, d: "f"))
h_d = make_horizontal_switch(lambda l, r: get_central_index(l, r, lambda t, d: "d"))

cb14_2 = make_vertical_switch(lambda t, d: (front2 if d == 0 else front2.T if t == 0 else h_n))
cb14_4 = make_vertical_switch(lambda t, d: (front if d == 0 else front.T if t == 0 else h_f))
cb14_6 = make_vertical_switch(lambda t, d: (front if d == 0 else front.T if t == 0 else h_d))

cb14 = StationTileSwitch("T", {2: cb14_2, 3: cb14_2, 4: cb14_4, 5: cb14_4, 6: cb14_6, 7: cb14_6})

traversable_station = AStation(
    id=0x02,
    translation_name="FLEXIBLE_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    disabled_platforms=0b1,
    callbacks={
        "select_tile_layout": cb24_0.to_index(None),
        "select_sprite_layout": grf.DualCallback(
            default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 4, cb24_0))
        ),
    },
)

traversable_station_no_side = AStation(
    id=0x03,
    translation_name="FLEXIBLE_NO_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    callbacks={
        "select_tile_layout": cb24_1.to_index(None),
        "select_sprite_layout": grf.DualCallback(
            default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 4, cb24_0))
        ),
    },
)
