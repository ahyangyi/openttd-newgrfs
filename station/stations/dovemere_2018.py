import grf
from station.lib import AStation, AMetaStation
from station.lib.parameters import parameter_list
from .dovemere_2018_lib.layouts import *
from .dovemere_2018_lib import demos, common_cb
from .dovemere_2018_lib.objects import objects
from .dovemere_2018_lib.roadstops import roadstops
from .dovemere_2018_lib.flexible_stations.semitraversable import semitraversable_stations
from .dovemere_2018_lib.flexible_stations.traversable import traversable_stations
from .dovemere_2018_lib.flexible_stations.side import side_stations
from .dovemere_2018_lib.flexible_stations.side_third import side_third_stations

modular_stations = []
for i, entry in enumerate(sorted(entries, key=lambda x: x.category)):
    modular_stations.append(
        AStation(
            id=0x1000 + i,
            translation_name="DEFAULT" if entry.traversable else "UNTRAVERSABLE",
            layouts=[entry, entry.M, entry.pushdown(9), entry.M.pushdown(9)],
            class_label=entry.category,
            cargo_threshold=40,
            non_traversable_tiles=0b00 if entry.traversable else 0b11,
            callbacks={
                "select_tile_layout": 0,
                "select_sprite_layout": grf.DualCallback(default=0, purchase=2),
                **common_cb,
            },
            is_waypoint="waypoint" in entry.notes,
            enable_if=[parameter_list.index("E88A9CA_ENABLE_MODULAR")],
            doc_layout=entry,
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
    [
        demos.normal_demo,
        demos.big_demo,
        demos.big_half_demo,
        demos.real_yard_demo,
        demos.full_auto_demo,
        demos.full_np_auto_demo,
        demos.semi_auto_demo,
        demos.semi_np_auto_demo,
        demos.side_auto_demo,
        demos.side_np_auto_demo,
        demos.side_third_auto_demo,
        demos.side_third_np_auto_demo,
        demos.special_demo_g,
        demos.special_demo_p,
        demos.special_demo_cn,
        demos.special_demo_sa,
        demos.special_demo_cp,
        demos.special_demo_aq,
    ],
    road_stops=roadstops,
    objects=objects,
)
