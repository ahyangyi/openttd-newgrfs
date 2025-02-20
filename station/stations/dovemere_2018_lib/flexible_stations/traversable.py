import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch, make_horizontal_switch
from ..layouts import named_tiles, layouts
from .. import common_cb, common_code
from .common import (
    determine_platform_odd,
    determine_platform_even,
    make_demo,
    make_row,
    make_front_row,
    make_central_row,
)
from station.stations.platforms import platform_classes, shelter_classes
from station.lib.parameters import parameter_list

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
        front[pclass][sclass] = make_front_row((pclass, sclass, "third_f"))

        h_n[pclass][sclass] = make_horizontal_switch(lambda l, r: make_central_row(l, r, (pclass, sclass, "n")))
        h_f[pclass][sclass] = make_horizontal_switch(lambda l, r: make_central_row(l, r, (pclass, sclass, "f")))
        h_d[pclass][sclass] = make_horizontal_switch(lambda l, r: make_central_row(l, r, (pclass, sclass, "d")))

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
    front = make_front_row((pclass, None, "platform"))
    for s, sclass in enumerate(shelter_classes):
        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_1 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        traversable_stations.append(
            AStation(
                id=0xFF20 + p * 0x4 + s,
                translation_name="FLEXIBLE_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                disabled_platforms=0b1,
                callbacks={
                    "select_tile_layout": cb24.to_index(),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].to_index(layouts), purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
                extra_code=common_code,
                enable_if=[
                    parameter_list["E88A9CA_ENABLE_TEMPLATE"],
                    parameter_list[f"PLATFORM_{pclass.upper()}"],
                    parameter_list[f"SHELTER_{sclass.upper()}"],
                ],
                doc_layout=demo_layout,
            )
        )

cb24 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True)
for p, pclass in enumerate(platform_classes):
    front = make_front_row((pclass, None, "platform"))
    for s, sclass in enumerate(shelter_classes):
        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_2 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        traversable_stations.append(
            AStation(
                id=0xFF30 + p * 0x4 + s,
                translation_name="FLEXIBLE_NO_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                disabled_platforms=0b100,
                callbacks={
                    "select_tile_layout": cb24.to_index(),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].to_index(layouts), purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
                extra_code=common_code,
                enable_if=[
                    parameter_list["E88A9CA_ENABLE_TEMPLATE"],
                    parameter_list[f"PLATFORM_{pclass.upper()}"],
                    parameter_list[f"SHELTER_{sclass.upper()}"],
                ],
                doc_layout=demo_layout,
            )
        )
