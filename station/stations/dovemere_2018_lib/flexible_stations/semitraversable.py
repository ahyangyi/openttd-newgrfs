import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch
from ..layouts import named_tiles, layouts
from .common import determine_platform_odd, determine_platform_even, make_front_row, make_demo, make_row
from .traversable import cb14_2, cb14_4, cb14_6


named_tiles.globalize()

front = make_front_row("_platform")
front2 = make_front_row("")

cb24_0 = make_vertical_switch(
    lambda t, d: 0 if t == 0 or d == 0 else {"n": 2, "f": 4, "d": 6}[determine_platform_odd(t, d)], cb24=True
)
cb24_1 = make_vertical_switch(
    lambda t, d: 0 if t == 0 or d == 0 else {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True
)

single = make_row(tiny, h_end_gate_untraversable, h_end_untraversable, h_normal, h_gate_full, h_gate_extender)
# XXX need "unreachable value" support
cb14_0a = make_vertical_switch(lambda t, d: single if d == t == 0 else front if d == 0 else front.T if t == 0 else tiny)
cb14_0b = make_vertical_switch(
    lambda t, d: single if d == t == 0 else front2 if d == 0 else front2.T if t == 0 else tiny
)

cb14a = StationTileSwitch(
    "T", {0: cb14_0a, 1: cb14_0a, 2: cb14_2, 3: cb14_2, 4: cb14_4, 5: cb14_4, 6: cb14_6, 7: cb14_6}
)
cb14b = StationTileSwitch(
    "T", {0: cb14_0b, 1: cb14_0b, 2: cb14_2, 3: cb14_2, 4: cb14_4, 5: cb14_4, 6: cb14_6, 7: cb14_6}
)

semitraversable_station = AStation(
    id=0x00,
    translation_name="FLEXIBLE_UNTRAVERSABLE_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b11,
    disabled_platforms=0b11,
    callbacks={
        "select_tile_layout": cb24_0.to_index(None),
        "select_sprite_layout": grf.DualCallback(
            default=cb14a.to_index(layouts), purchase=layouts.index(make_demo(cb14a, 4, 4, cb24_0))
        ),
    },
)

semitraversable_station_no_side = AStation(
    id=0x01,
    translation_name="FLEXIBLE_UNTRAVERSABLE_NO_SIDE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b11,
    disabled_platforms=0b111,
    callbacks={
        "select_tile_layout": cb24_1.to_index(None),
        "select_sprite_layout": grf.DualCallback(
            default=cb14b.to_index(layouts), purchase=layouts.index(make_demo(cb14b, 4, 4, cb24_1))
        ),
    },
)
