import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch, make_horizontal_switch
from ..layouts import named_tiles, layouts
from .. import common_cb
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


def fill_odd(d):
    return {**d, **{k + 1: v for k, v in d.items()}}


front = {pclass: {} for pclass in platform_classes}
front2 = {}
single = {}
h_n = {pclass: {} for pclass in platform_classes}
h_f = {pclass: {} for pclass in platform_classes}
h_d = {pclass: {} for pclass in platform_classes}
cb14_2 = {pclass: {} for pclass in platform_classes}
cb14_4 = {pclass: {} for pclass in platform_classes}
cb14_6 = {pclass: {} for pclass in platform_classes}
cb14 = {pclass: {} for pclass in platform_classes}
for pclass in platform_classes:
    pclass_desc = "_" + pclass
    front2[pclass] = make_front_row((pclass, None, "third"))
    single[pclass] = make_row(
        named_tiles[("tiny", pclass, None, "corridor")],
        named_tiles[("h_end_gate", pclass, None, "corridor")],
        named_tiles[("h_end", pclass, None, "corridor")],
        named_tiles[("h_normal", pclass, None, "corridor")],
        named_tiles[("h_gate", pclass, None, "corridor")],
        named_tiles[("h_gate_extender", pclass, None, "corridor")],
    )
    for sclass in shelter_classes:
        sclass_desc = "" if sclass == "shelter_1" else "_" + sclass
        front[pclass][sclass] = make_front_row(
            pclass_desc + sclass_desc + "_third_f", fallback_suffix=pclass_desc + "_third_f"
        )

        h_n[pclass][sclass] = make_horizontal_switch(
            lambda l, r: make_central_row(l, r, pclass_desc + sclass_desc + "_n", pclass_desc + "_n")
        )
        h_f[pclass][sclass] = make_horizontal_switch(
            lambda l, r: make_central_row(l, r, pclass_desc + sclass_desc + "_f", pclass_desc + "_f")
        )
        h_d[pclass][sclass] = make_horizontal_switch(
            lambda l, r: make_central_row(l, r, pclass_desc + sclass_desc + "_d", pclass_desc + "_d")
        )

        cb14_2[pclass][sclass] = make_vertical_switch(
            lambda t, d: (
                single[pclass]
                if d == t == 0
                else front2[pclass] if d == 0 else front[pclass][sclass].T if t == 0 else h_n[pclass][sclass]
            )
        )
        cb14_4[pclass][sclass] = make_vertical_switch(
            lambda t, d: (
                single[pclass]
                if d == t == 0
                else front[pclass][sclass] if d == 0 else front2[pclass].T if t == 0 else h_f[pclass][sclass]
            )
        )
        cb14_6[pclass][sclass] = make_vertical_switch(
            lambda t, d: (
                single[pclass]
                if d == t == 0
                else front[pclass][sclass] if d == 0 else front[pclass][sclass].T if t == 0 else h_d[pclass][sclass]
            )
        )

        cb14[pclass][sclass] = StationTileSwitch(
            "T", fill_odd({2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass], 6: cb14_6[pclass][sclass]})
        )

traversable_stations = []

cb24 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_odd(t, d)], cb24=True)
for p, pclass in enumerate(platform_classes):
    pclass_desc = "_" + pclass
    front = make_front_row(pclass_desc + "_platform")
    for s, sclass in enumerate(shelter_classes):
        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_1 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        traversable_stations.append(
            AStation(
                id=0x300 + p * 0x10 + s,
                translation_name="FLEXIBLE_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                disabled_platforms=0b1,
                callbacks={
                    "select_tile_layout": cb24.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].to_index(layouts), purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
                doc_layout=demo_layout,
            )
        )

cb24 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True)
for p, pclass in enumerate(platform_classes):
    pclass_desc = "_" + pclass
    front = make_front_row(pclass_desc + "_platform")
    for s, sclass in enumerate(shelter_classes):
        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_2 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        traversable_stations.append(
            AStation(
                id=0x400 + p * 0x10 + s,
                translation_name="FLEXIBLE_NO_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                disabled_platforms=0b100,
                callbacks={
                    "select_tile_layout": cb24.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].to_index(layouts), purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
                doc_layout=demo_layout,
            )
        )
