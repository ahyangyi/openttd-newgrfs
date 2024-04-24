from station.lib import AStation, AMetaStation
from .dovemere_2018_lib.layouts import *
from .dovemere_2018_lib import demos
from .dovemere_2018_lib.flexible_stations.semitraversable import (
    semitraversable_station,
    semitraversable_station_no_side,
)
from .dovemere_2018_lib.flexible_stations.traversable import traversable_station, traversable_station_no_side
from .dovemere_2018_lib.flexible_stations.side import (
    side_station,
    back_side_station,
    side_station_np,
    back_side_station_np,
)
from .dovemere_2018_lib.flexible_stations.side_third import (
    side_third_station,
    back_side_third_station,
    side_third_station_np,
    back_side_third_station_np,
)


the_stations = AMetaStation(
    [
        semitraversable_station,
        semitraversable_station_no_side,
        traversable_station,
        traversable_station_no_side,
        side_station,
        back_side_station,
        side_station_np,
        back_side_station_np,
        side_third_station,
        back_side_third_station,
        side_third_station_np,
        back_side_third_station_np,
    ]
    + [
        AStation(
            id=0x10 + i,
            translation_name="DEFAULT" if entry.traversable else "UNTRAVERSABLE",
            layouts=[entry, entry.M],
            class_label=entry.category,
            cargo_threshold=40,
            non_traversable_tiles=0b00 if entry.traversable else 0b11,
            callbacks={"select_tile_layout": 0},
        )
        for i, entry in enumerate(sorted(entries, key=lambda x: x.category))
    ],
    b"\xe8\x8a\x9cA",
    [
        b"\xe8\x8a\x9c" + x
        for x in [b"A"]
        + [(r * 16 + c).to_bytes(1, "little") for r in [8] for c in range(16)]
        + [b"\xF0"]
        + [(r * 16 + c).to_bytes(1, "little") for r in [9, 10, 11, 12] for c in [0, 1, 2, 3]]
        + [b"\xF1", b"\xF2"]
    ],
    flexible_entries + entries,
    [
        demos.normal_demo,
        demos.big_demo,
        demos.big_half_demo,
        demos.real_yard_demo,
        demos.full_auto_demo,
        demos.semi_auto_demo,
        demos.side_auto_demo,
        demos.side_third_auto_demo,
        demos.special_demo_g,
        demos.special_demo_p,
        demos.special_demo_cn,
        demos.special_demo_sa,
        demos.special_demo_cp,
        demos.special_demo_aq,
    ],
)
