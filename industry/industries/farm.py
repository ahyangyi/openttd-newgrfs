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
    name="Farm",
    override_type=0x09,
    layouts=SplitDefinition(
        9,
        {
            0: transcribe(large_set, tile_map),
            1: transcribe(large_set, tile_map),
            2: transcribe(large_set, tile_map),
            3: transcribe(medium_set, tile_map),
            4: transcribe(small_set, tile_map),
            5: transcribe(tiny_set, tile_map),
            6: transcribe(one_tile_set, tile_map),
            7: [[{"xofs": 0, "yofs": 0, "gfx": grf.NewIndustryTileID(0x23)}]],
        },
    ),
    mapgen_probability=15,
    ingame_probability=4,
)
