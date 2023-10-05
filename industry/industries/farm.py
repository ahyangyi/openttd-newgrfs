import grf
from industry.lib.industry import AIndustry, SplitDefinition, transcribe, symmetrize

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
    substitute_type=0x09,
    layouts=SplitDefinition(
        {
            0: transcribe(medium_set, tile_map),
            1: transcribe(medium_set, tile_map),
            2: transcribe(medium_set, tile_map),
            3: transcribe(medium_set, tile_map),
            4: transcribe(tiny_set, tile_map),
            5: transcribe(one_tile_set, tile_map),
            6: [[{"xofs": 0, "yofs": 0, "gfx": grf.NewIndustryTileID(0x23)}]],
        }
    ),
)
