import grf
from station.lib import AStation, AMetaStation
from station.lib.parameters import parameter_list
from .dovemere_2018_lib.layouts import *
from .dovemere_2018_lib import demos, common_cb, common_code, Registers
from .dovemere_2018_lib.objects import objects
from .dovemere_2018_lib.roadstops import roadstops
from .dovemere_2018_lib.flexible_stations.semitraversable import semitraversable_stations
from .dovemere_2018_lib.flexible_stations.traversable import traversable_stations
from .dovemere_2018_lib.flexible_stations.side import side_stations
from .dovemere_2018_lib.flexible_stations.side_third import side_third_stations
from agrf.strings import String

modular_stations = []
for i, entry in enumerate(sorted(entries, key=lambda x: x.category)):
    enable_if = [parameter_list["E88A9CA_ENABLE_MODULAR"]]
    for platform_class in ["concrete", "brick"]:
        if platform_class in entry.notes:
            enable_if.append(parameter_list[f"PLATFORM_{platform_class.upper()}"])
    for shelter_class in ["shelter_1", "shelter_2"]:
        if shelter_class in entry.notes:
            enable_if.append(parameter_list[f"SHELTER_{shelter_class.upper()}"])

    has_track = entry.traversable
    far_platform = entry.category[-1] in {
        0x81,
        0x83,
        0x85,
        0x87,
        0x92,
        0x93,
        0xA2,
        0xA3,
        0xA6,
        0xA7,
        0xAA,
        0xAB,
        0xAE,
        0xAF,
        0xB2,
        0xB3,
        0xB6,
        0xB7,
        0xC2,
        0xC3,
        0xC6,
        0xC7,
    }
    near_platform = entry.category[-1] in {
        0x89,
        0x8B,
        0x8D,
        0x8F,
        0x91,
        0x93,
        0xA1,
        0xA3,
        0xA5,
        0xA7,
        0xA9,
        0xAB,
        0xAD,
        0xAF,
        0xB1,
        0xB3,
        0xB5,
        0xB7,
        0xC1,
        0xC3,
        0xC5,
        0xC7,
    }
    translation_name = String("STR_STATION_TEMPLATE")(
        f"STR_PART_TRACK_{str(has_track).upper()}",
        f"STR_PART_NPLAT_{str(far_platform).upper()}",
        f"STR_PART_SPLAT_{str(near_platform).upper()}",
    )

    modular_stations.append(
        AStation(
            id=entry.id,
            translation_name=translation_name,
            layouts=[
                entry,
                entry.M,
                entry.squash(0.6).pushdown(3).filter_register(Registers.SNOW),
                entry.M.squash(0.6).pushdown(3).filter_register(Registers.SNOW),
            ],
            class_label=entry.category,
            cargo_threshold=40,
            non_traversable_tiles=0b00 if entry.traversable else 0b11,
            callbacks={
                "select_tile_layout": 0,
                "select_sprite_layout": grf.DualCallback(default=0, purchase=2),
                **common_cb,
            },
            is_waypoint="waypoint" in entry.notes,
            enable_if=enable_if,
            doc_layout=entry,
            extra_code=common_code,
        )
    )


the_stations = AMetaStation(
    semitraversable_stations + traversable_stations + side_stations + side_third_stations + modular_stations,
    b"\xe8\x8a\x9cA",
    [
        b"\xe8\x8a\x9c" + x
        for x in [b"A"]
        + [(r * 16 + c).to_bytes(1, "little") for r in [8] for c in range(16)]
        + [(r * 16 + c).to_bytes(1, "little") for r in [9] for c in range(4)]
        + [x.to_bytes(1, "little") for x in range(0xA0, 0xB0)]
        + [x.to_bytes(1, "little") for x in range(0xB0, 0xB8)]
        + [x.to_bytes(1, "little") for x in range(0xC0, 0xC8)]
        + [b"\xF0"]
        + [b"R", b"Z"]
    ],
    {
        "Realistic Layouts": demos.realistic_demos,
        "Template Showcases": demos.template_demos,
        "Diverse Designs": demos.special_demos,
        "Station Square": demos.plaza_demos,
        "With Other NewGRF": demos.third_party_demos,
    },
    road_stops=roadstops,
)
