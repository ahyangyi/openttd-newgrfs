import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch, make_horizontal_switch
from ..layouts import named_tiles, layouts
from .common import (
    determine_platform_odd,
    determine_platform_even,
    make_demo,
    make_row,
    make_front_row,
    make_central_row,
)

named_tiles.globalize()


front = make_front_row("_third_f")
front2 = make_front_row("_third")


single = make_row(
    tiny_corridor, h_end_gate_corridor, h_end_corridor, h_normal_corridor, h_gate_corridor, h_gate_extender_corridor
)


cb24_0 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_odd(t, d)], cb24=True)
cb24_1 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True)

h_n = make_horizontal_switch(lambda l, r: make_central_row(l, r, "n"))
h_f = make_horizontal_switch(lambda l, r: make_central_row(l, r, "f"))
h_d = make_horizontal_switch(lambda l, r: make_central_row(l, r, "d"))

cb14_2 = make_vertical_switch(
    lambda t, d: (single if d == t == 0 else front2 if d == 0 else front.T if t == 0 else h_n)
)
cb14_4 = make_vertical_switch(
    lambda t, d: (single if d == t == 0 else front if d == 0 else front2.T if t == 0 else h_f)
)
cb14_6 = make_vertical_switch(lambda t, d: (single if d == t == 0 else front if d == 0 else front.T if t == 0 else h_d))

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
    disabled_platforms=0b100,
    callbacks={
        "select_tile_layout": cb24_1.to_index(None),
        "select_sprite_layout": grf.DualCallback(
            default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 4, cb24_0))
        ),
    },
)
