import grf
from station.lib import AStation, AMetaStation
from agrf.magic import Switch
from .dovemere_2018_lib.layouts import *
from .dovemere_2018_lib.demos import *
from .dovemere_2018_lib.flexible_stations.semi_auto import flex0
from .dovemere_2018_lib.flexible_stations.full_auto import flex1


the_stations = AMetaStation(
    [flex0, flex1]
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
        for i, entry in enumerate(entries)
    ],
    b"\xe8\x8a\x9cA",
    [
        b"\xe8\x8a\x9c" + x
        for x in [(r * 16 + c).to_bytes(1, "little") for r in [8] for c in range(16)]
        + [b"\xF1"]
        + [(r * 16 + c).to_bytes(1, "little") for r in [9, 10, 11, 12] for c in [0, 1, 2, 3]]
        + [b"\xF1", b"\xF2"]
    ],
    entries,
    [
        normal_demo,
        big_demo,
        big_half_demo,
        real_yard_demo,
        full_auto_demo,
        semi_auto_demo,
        side_auto_demo,
        special_demo_g,
        special_demo_p,
        special_demo_cn,
        special_demo_sa,
        special_demo_cp,
        special_demo_aq,
    ],
)
