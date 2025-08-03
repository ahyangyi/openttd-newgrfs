import grf
from station.lib import AStation, AMetaStation

station = AStation(
    id=0x0000,
    translation_name="CONCRETE_GROUND",
    layouts=[entry],
    class_label=b"\xe5\xbc\x8bf",
    cargo_threshold=40,
    non_traversable_tiles=0b11,
    doc_layout=entry,
)


ground_stations = AMetaStation(
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
        + [b"\xf0"]
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
