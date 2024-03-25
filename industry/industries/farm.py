import grf
from industry.lib.industry import (
    AIndustry,
    SplitDefinition,
    transcribe,
    symmetrize,
    OldIndustryTileID,
    NewIndustryTileID,
)

large_set = symmetrize(
    [
        (
            "cddc",
            "cddc",
            "cabc",
            "eeff",
            "eeff",
        ),
        (
            "ddeec",
            "ddefc",
            "cffff",
            "abecf",
        ),
    ]
)

medium_set = symmetrize(
    [
        (
            "eed",
            "abd",
            "cff",
        ),
        (
            "cddc",
            "eabf",
            "eeff",
        ),
        (
            "ddee",
            "cffe",
            "abec",
        ),
    ]
)

small_set = symmetrize(
    [
        (
            "abd",
            "ecf",
        ),
    ]
)

tiny_set = [
    ("ab",),
]

one_tile_set = [
    ("a",),
]

tile_map = {
    "a": OldIndustryTileID(0x21),  # house (left)
    "b": OldIndustryTileID(0x22),  # house (right)
    "c": OldIndustryTileID(0x23),  # warehouse with straws
    "d": OldIndustryTileID(0x24),  # warehouse
    "e": OldIndustryTileID(0x25),  # silo
    "f": OldIndustryTileID(0x26),  # piggery
}

the_industry = AIndustry(
    translation_name="FARM",
    override_type=0x09,
    layouts=SplitDefinition(
        ("INDUSTRY_SIZE",),
        {
            ("ENORMOUS",): transcribe(large_set, tile_map),
            ("HUGE",): transcribe(large_set, tile_map),
            ("LARGE",): transcribe(large_set, tile_map),
            ("MEDIUM",): transcribe(medium_set, tile_map),
            ("SMALL",): transcribe(small_set, tile_map),
            ("TINY",): transcribe(tiny_set, tile_map),
            ("ONE_TILE",): transcribe(one_tile_set, tile_map),
            ("ONE_TILE_FLAT",): [grf.IndustryLayout([NewIndustryTileID(0x23)(0, 0)])],
        },
    ),
    mapgen_probability=15,
    ingame_probability=4,
)
