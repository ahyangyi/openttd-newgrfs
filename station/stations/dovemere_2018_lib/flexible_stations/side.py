import grf
from station.lib import AStation, make_horizontal_switch
from .. import common_properties
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
        named_tiles[f"tiny_asym{pclass_desc}_platform"],
        named_tiles[f"h_end_asym_gate{suffix}_platform"],
        named_tiles[f"h_end_asym{suffix}_platform"],
        named_tiles[f"h_normal{pclass_desc}_platform"],
        named_tiles[f"h_gate_1{pclass_desc}_platform"],
        named_tiles[f"h_gate_extender_1{pclass_desc}_platform"],
    )


cb14 = {
    pclass: {
        sclass: make_horizontal_switch(lambda l, r, pclass=pclass, sclass=sclass: get_side_index(l, r, pclass, sclass))
        for sclass in shelter_classes
    }
    for pclass in platform_classes
}


side_stations = []

for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        if pclass == "concrete" and sclass == "shelter_1":
            side_station_demo = lambda r, c, cb14=cb14[pclass][sclass]: cb14.demo(r, c)
        side_stations.append(
            AStation(
                id=0x500 + p * 0x10 + s,
                translation_name="FLEXIBLE_FRONT_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                disabled_platforms=0b11111110,
                callbacks={
                    "select_tile_layout": 0,
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].to_index(layouts),
                        purchase=layouts.index(make_demo(cb14[pclass][sclass], 4, 1)),
                    ),
                    **common_cb,
                },
            )
        )

for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        if pclass == "concrete" and sclass == "shelter_1":
            back_side_station_demo = lambda r, c, cb14=cb14[pclass][sclass]: cb14.T.demo(r, c)
        side_stations.append(
            AStation(
                id=0x600 + p * 0x10 + s,
                translation_name="FLEXIBLE_BACK_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                disabled_platforms=0b11111110,
                callbacks={
                    "select_tile_layout": 0,
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].T.to_index(layouts),
                        purchase=layouts.index(make_demo(cb14[pclass][sclass].T, 4, 1)),
                    ),
                    **common_cb,
                },
            )
        )


def get_side_index(l, r):
    return horizontal_layout(l, r, tiny_asym, h_end_asym_gate, h_end_asym, h_normal, h_gate_1, h_gate_extender_1)


cb14 = make_horizontal_switch(get_side_index)

side_station_np_demo = lambda r, c, cb14=cb14: cb14.demo(r, c)
side_stations.append(
    AStation(
        id=0x700,
        translation_name="FLEXIBLE_FRONT_SIDE_NP",
        layouts=layouts,
        class_label=b"\xe8\x8a\x9cA",
        **common_properties,
        non_traversable_tiles=0b11,
        disabled_platforms=0b11111110,
        callbacks={
            "select_tile_layout": 0,
            "select_sprite_layout": grf.DualCallback(
                default=cb14.to_index(layouts), purchase=layouts.index(make_demo(cb14, 4, 1))
            ),
            **common_cb,
        },
    )
)
back_side_station_np_demo = lambda r, c, cb14=cb14: cb14.T.demo(r, c)
side_stations.append(
    AStation(
        id=0x701,
        translation_name="FLEXIBLE_BACK_SIDE_NP",
        layouts=layouts,
        class_label=b"\xe8\x8a\x9cA",
        **common_properties,
        non_traversable_tiles=0b11,
        disabled_platforms=0b11111110,
        callbacks={
            "select_tile_layout": 0,
            "select_sprite_layout": grf.DualCallback(
                default=cb14.T.to_index(layouts), purchase=layouts.index(make_demo(cb14.T, 4, 1))
            ),
            **common_cb,
        },
    )
)
