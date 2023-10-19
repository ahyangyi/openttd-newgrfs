import grf
from industry.lib.industry import AIndustry, SplitDefinition, transcribe, symmetrize


large_set = symmetrize(
    [
        (
            "x   ",
            "x   ",
            "xx  ",
            " xxx",
        ),
        (
            "xx  ",
            "x  x",
            "  xx",
            "  x ",
        ),
    ]
)
medium_set = symmetrize(
    [
        (
            "x  ",
            "x  ",
            "xxx",
        ),
        (
            "x  ",
            "xx ",
            " xx",
        ),
        (
            "x   ",
            "xx  ",
            "  xx",
        ),
        (
            " x  ",
            "xxx ",
            "   x",
        ),
        (
            " x  ",
            "x x ",
            "x  x",
        ),
        (
            "x   ",
            "x   ",
            "x xx",
        ),
    ]
)

small_set = symmetrize(
    [
        (
            "x ",
            "xx",
            "x ",
        ),
    ]
)

tiny_set = symmetrize(
    [
        (
            "x  ",
            "  x",
        ),
    ]
)

one_tile_set = [
    ("x",),
]

tile_map = {"x": grf.OldIndustryTileID(0x1D)}

the_industry = AIndustry(
    name="Oil Wells",
    override_type=0x0B,
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
    mapgen_probability=6,
    ingame_probability=6,
)
