import grf
from station.lib import AStation, make_horizontal_switch
from ..layouts import named_tiles, layouts
from .. import common_cb
from .common import make_demo, horizontal_layout
from station.stations.platforms import platform_classes, shelter_classes

named_tiles.globalize()


def get_side_index(l, r, pclass, sclass):
    pclass_desc = "" if pclass == "concrete" else "_" + pclass
    sclass_desc = "" if sclass == "shelter_1" else "_" + sclass
    suffix = pclass_desc + sclass_desc
    return horizontal_layout(
        l,
        r,
        named_tiles[f"tiny_asym{pclass_desc}_third_f"],
        named_tiles[f"h_end_asym_gate{suffix}_third_f"],
        named_tiles[f"h_end_asym{suffix}_third_f"],
        named_tiles[f"h_normal{pclass_desc}_third_f"],
        named_tiles[f"h_gate_1{pclass_desc}_third_f"],
        named_tiles[f"h_gate_extender_1{pclass_desc}_third_f"],
    )


cb14 = {
    pclass: {
        sclass: make_horizontal_switch(lambda l, r, pclass=pclass, sclass=sclass: get_side_index(l, r, pclass, sclass))
        for sclass in shelter_classes
    }
    for pclass in platform_classes
}

side_third_stations = []

for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        if pclass == "concrete" and sclass == "shelter_2":
            side_third_station_demo = lambda r, c, cb14=cb14[pclass][sclass]: cb14.demo(r, c)
        demo_layout = make_demo(cb14[pclass][sclass], 4, 1)
        demo_layout.station_id = 0x800 + p * 0x10 + s
        if p > 0 or s > 0:
            demo_layout.notes.append("noshow")
        side_third_stations.append(
            AStation(
                id=0x800 + p * 0x10 + s,
                translation_name="FLEXIBLE_FRONT_SIDE_THIRD",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                disabled_platforms=0b11111110,
                callbacks={
                    "select_tile_layout": 0,
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].to_index(layouts), purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
            )
        )

for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        if pclass == "concrete" and sclass == "shelter_2":
            back_side_third_station_demo = lambda r, c, cb14=cb14[pclass][sclass]: cb14.T.demo(r, c)
        demo_layout = make_demo(cb14[pclass][sclass].T, 4, 1)
        demo_layout.station_id = 0x900 + p * 0x10 + s
        if p > 0 or s > 0:
            demo_layout.notes.append("noshow")
        side_third_stations.append(
            AStation(
                id=0x900 + p * 0x10 + s,
                translation_name="FLEXIBLE_BACK_SIDE_THIRD",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                disabled_platforms=0b11111110,
                callbacks={
                    "select_tile_layout": 0,
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].T.to_index(layouts), purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
            )
        )


def get_side_index(l, r, pclass):
    suffix = "" if pclass == "concrete" else "_" + pclass
    return horizontal_layout(
        l,
        r,
        named_tiles[f"tiny_asym{suffix}_third"],
        named_tiles[f"h_end_asym_gate{suffix}_third"],
        named_tiles[f"h_end_asym{suffix}_third"],
        named_tiles[f"h_normal{suffix}_third"],
        named_tiles[f"h_gate_1{suffix}_third"],
        named_tiles[f"h_gate_extender_1{suffix}_third"],
    )


cb14 = {
    pclass: make_horizontal_switch(lambda l, r, pclass=pclass: get_side_index(l, r, pclass))
    for pclass in platform_classes
}

for p, pclass in enumerate(platform_classes):
    if pclass == "concrete":
        side_third_station_np_demo = lambda r, c, cb14=cb14[pclass]: cb14.demo(r, c)
    demo_layout = make_demo(cb14[pclass], 4, 1)
    demo_layout.station_id = 0x780 + p
    if p > 0:
        demo_layout.notes.append("noshow")

    side_third_stations.append(
        AStation(
            id=0x780 + p,
            translation_name="FLEXIBLE_FRONT_SIDE_THIRD_NP",
            layouts=layouts,
            class_label=b"\xe8\x8a\x9cA",
            cargo_threshold=40,
            disabled_platforms=0b11111110,
            callbacks={
                "select_tile_layout": 0,
                "select_sprite_layout": grf.DualCallback(
                    default=cb14[pclass].to_index(layouts), purchase=layouts.index(demo_layout)
                ),
                **common_cb,
            },
        )
    )

for p, pclass in enumerate(platform_classes):
    if pclass == "concrete":
        back_side_third_station_np_demo = lambda r, c, cb14=cb14[pclass]: cb14.demo(r, c)
    demo_layout = make_demo(cb14[pclass].T, 4, 1)
    demo_layout.station_id = 0x790 + p
    if p > 0:
        demo_layout.notes.append("noshow")

    side_third_stations.append(
        AStation(
            id=0x790 + p,
            translation_name="FLEXIBLE_BACK_SIDE_THIRD_NP",
            layouts=layouts,
            class_label=b"\xe8\x8a\x9cA",
            cargo_threshold=40,
            disabled_platforms=0b11111110,
            callbacks={
                "select_tile_layout": 0,
                "select_sprite_layout": grf.DualCallback(
                    default=cb14[pclass].T.to_index(layouts), purchase=layouts.index(demo_layout)
                ),
                **common_cb,
            },
        )
    )
