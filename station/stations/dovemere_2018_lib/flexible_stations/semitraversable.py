import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch
from ..layouts import named_tiles, layouts
from .common import determine_platform_odd, determine_platform_even, make_front_row, make_demo, make_row
from .traversable import cb14_2, cb14_4, cb14_6, fill_odd
from station.stations.platforms import platform_classes, shelter_classes


named_tiles.globalize()


single = make_row(tiny_untraversable, h_end_gate_untraversable, h_end_untraversable, h_normal, h_gate, h_gate_extender)

semitraversable_stations = []
global_id = 0x100
for pclass in platform_classes:
    pclass_desc = "" if pclass == "concrete" else "_" + pclass
    front = make_front_row(pclass_desc + "_platform")
    for sclass in shelter_classes:
        cb24 = make_vertical_switch(
            lambda t, d: 0 if t == 0 or d == 0 else {"n": 2, "f": 4, "d": 6}[determine_platform_odd(t, d)], cb24=True
        )
        cb14_0 = make_vertical_switch(
            lambda t, d: single if d == t == 0 else front if d == 0 else front.T if t == 0 else None
        )
        cb14 = StationTileSwitch(
            "T", fill_odd({0: cb14_0, 2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass], 6: cb14_6[pclass][sclass]})
        )
        if pclass == "concrete" and sclass == "shelter_1":
            demo_1 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        semitraversable_stations.append(
            AStation(
                id=global_id,
                translation_name="FLEXIBLE_UNTRAVERSABLE_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                disabled_platforms=0b11,
                callbacks={
                    "select_tile_layout": cb24.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 4, cb24))
                    ),
                },
            )
        )
        global_id += 1

front = make_front_row("")
for pclass in platform_classes:
    for sclass in shelter_classes:
        cb24 = make_vertical_switch(
            lambda t, d: 0 if t == 0 or d == 0 else {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True
        )
        cb14_0 = make_vertical_switch(
            lambda t, d: single if d == t == 0 else front if d == 0 else front.T if t == 0 else None
        )
        cb14 = StationTileSwitch(
            "T", fill_odd({0: cb14_0, 2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass], 6: cb14_6[pclass][sclass]})
        )
        if pclass == "concrete" and sclass == "shelter_1":
            demo_2 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        semitraversable_stations.append(
            AStation(
                id=global_id,
                translation_name="FLEXIBLE_UNTRAVERSABLE_NO_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                disabled_platforms=0b111,
                callbacks={
                    "select_tile_layout": cb24.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 4, cb24))
                    ),
                },
            )
        )
        global_id += 1
