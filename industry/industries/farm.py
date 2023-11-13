import grf
from industry.lib.industry import AIndustry, SplitDefinition, transcribe, symmetrize

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
    "a": grf.OldIndustryTileID(0x21),  # house (left)
    "b": grf.OldIndustryTileID(0x22),  # house (right)
    "c": grf.OldIndustryTileID(0x23),  # warehouse with straws
    "d": grf.OldIndustryTileID(0x24),  # warehouse
    "e": grf.OldIndustryTileID(0x25),  # silo
    "f": grf.OldIndustryTileID(0x26),  # piggery
}

the_industry = AIndustry(
    translation_name="FARM",
    override_type=0x09,
    layouts=SplitDefinition(
        "INDUSTRY_SIZE",
        {
            "ENORMOUS": transcribe(large_set, tile_map),
            "HUGE": transcribe(large_set, tile_map),
            "LARGE": transcribe(large_set, tile_map),
            "MEDIUM": transcribe(medium_set, tile_map),
            "SMALL": transcribe(small_set, tile_map),
            "TINY": transcribe(tiny_set, tile_map),
            "ONE_TILE": transcribe(one_tile_set, tile_map),
            "ONE_TILE_FLAT": [[{"xofs": 0, "yofs": 0, "gfx": grf.NewIndustryTileID(0x23)}]],
        },
    ),
    mapgen_probability=15,
    ingame_probability=4,
)
