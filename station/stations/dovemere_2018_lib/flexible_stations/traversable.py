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
from station.stations.platforms import platform_classes, shelter_classes

named_tiles.globalize()

front = {}
front2 = {}
single = {}
for pclass in platform_classes:
    pclass_desc = "" if pclass == "concrete" else "_" + pclass
    front[pclass] = {}
    front2[pclass] = make_front_row(pclass_desc + "_third")
    single[pclass] = make_row(
        tiny_corridor, h_end_gate_corridor, h_end_corridor, h_normal_corridor, h_gate_corridor, h_gate_extender_corridor
    )  # FIXME
    for sclass in shelter_classes:
        sclass_desc = "" if sclass == "shelter_1" else "_" + sclass
        front[pclass][sclass] = make_front_row(
            sclass_desc + pclass_desc + "_third_f", fallback_suffix=pclass_desc + "_third_f"
        )


h_n = make_horizontal_switch(lambda l, r: make_central_row(l, r, "n"))
h_f = make_horizontal_switch(lambda l, r: make_central_row(l, r, "f"))
h_d = make_horizontal_switch(lambda l, r: make_central_row(l, r, "d"))

cb14_2 = make_vertical_switch(
    lambda t, d: (
        single["concrete"]
        if d == t == 0
        else front2["concrete"] if d == 0 else front["concrete"]["shelter_1"].T if t == 0 else h_n
    )
)
cb14_4 = make_vertical_switch(
    lambda t, d: (
        single["concrete"]
        if d == t == 0
        else front["concrete"]["shelter_1"] if d == 0 else front2["concrete"].T if t == 0 else h_f
    )
)
cb14_6 = make_vertical_switch(
    lambda t, d: (
        single["concrete"]
        if d == t == 0
        else front["concrete"]["shelter_1"] if d == 0 else front["concrete"]["shelter_1"].T if t == 0 else h_d
    )
)

cb14 = StationTileSwitch("T", {2: cb14_2, 3: cb14_2, 4: cb14_4, 5: cb14_4, 6: cb14_6, 7: cb14_6})

traversable_stations = []
global_id = 0x08

cb24 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_odd(t, d)], cb24=True)
for pclass in platform_classes:
    pclass_desc = "" if pclass == "concrete" else "_" + pclass
    front = make_front_row(pclass_desc + "_platform")
    for sclass in shelter_classes:
        if pclass == "concrete" and sclass == "shelter_1":
            demo_1 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        traversable_stations.append(
            AStation(
                id=global_id,
                translation_name="FLEXIBLE_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                disabled_platforms=0b1,
                callbacks={
                    "select_tile_layout": cb24.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 4, cb24))
                    ),
                },
            )
        )
        global_id += 1

cb24 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True)
for pclass in platform_classes:
    pclass_desc = "" if pclass == "concrete" else "_" + pclass
    front = make_front_row(pclass_desc + "_platform")
    for sclass in shelter_classes:
        if pclass == "concrete" and sclass == "shelter_1":
            demo_2 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        traversable_stations.append(
            AStation(
                id=global_id,
                translation_name="FLEXIBLE_NO_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                disabled_platforms=0b100,
                callbacks={
                    "select_tile_layout": cb24.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 4, cb24))
                    ),
                },
            )
        )
        global_id += 1
