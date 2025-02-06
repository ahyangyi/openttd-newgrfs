import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch
from .. import common_cb, common_code
from ..layouts import named_tiles, layouts
from .common import determine_platform_odd, determine_platform_even, make_front_row, make_demo, make_row
from .traversable import cb14_2, cb14_4, cb14_6, fill_odd
from station.stations.platforms import platform_classes, shelter_classes
from station.lib.parameters import parameter_list


named_tiles.globalize()


single = make_row(tiny_untraversable, h_end_gate_untraversable, h_end_untraversable, h_normal, h_gate, h_gate_extender)

semitraversable_stations = []
for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        front = make_front_row((pclass, sclass, "platform"))
        cb24 = make_vertical_switch(
            lambda t, d: 0 if t == 0 or d == 0 else {"n": 2, "f": 4, "d": 6}[determine_platform_odd(t, d)], cb24=True
        )
        cb14_0 = make_vertical_switch(
            lambda t, d: single if d == t == 0 else front if d == 0 else front.T if t == 0 else None
        )
        cb14 = StationTileSwitch(
            "T", fill_odd({0: cb14_0, 2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass], 6: cb14_6[pclass][sclass]})
        )
        demo_layout = make_demo(cb14, 4, 4, cb24)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_1 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        semitraversable_stations.append(
            AStation(
                id=0xFF00 + p * 0x4 + s,
                translation_name="FLEXIBLE_UNTRAVERSABLE_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                disabled_platforms=0b11,
                callbacks={
                    "select_tile_layout": cb24.to_index(),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(demo_layout)
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

front = make_front_row((None, None, ""))
for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        cb24 = make_vertical_switch(
            lambda t, d: 0 if t == 0 or d == 0 else {"n": 2, "f": 4, "d": 6}[determine_platform_even(t, d)], cb24=True
        )
        cb14_0 = make_vertical_switch(
            lambda t, d: single if d == t == 0 else front if d == 0 else front.T if t == 0 else None
        )
        cb14 = StationTileSwitch(
            "T", fill_odd({0: cb14_0, 2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass], 6: cb14_6[pclass][sclass]})
        )

        demo_layout = make_demo(cb14, 4, 4, cb24)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_2 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")

        semitraversable_stations.append(
            AStation(
                id=0xFF10 + p * 0x4 + s,
                translation_name="FLEXIBLE_UNTRAVERSABLE_NO_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                disabled_platforms=0b111,
                callbacks={
                    "select_tile_layout": cb24.to_index(),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(demo_layout)
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
