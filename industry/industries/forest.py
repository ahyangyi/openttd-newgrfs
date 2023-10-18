import grf
from industry.lib.industry import AIndustry, SplitDefinition, transcribe, symmetrize

huge_set = symmetrize(
    [
        (
            " xxxxxx ",
            "xxxxxxxx",
            "xxxxxxxx",
            "xxxxxxxx",
            "xxxxxxxx",
            "xxxxxxxx",
            "xxxxxxxx",
            "xxxxxxxx",
            " xxxxxx ",
        ),
    ]
)

large_set = symmetrize(
    [
        (
            " xxxx ",
            "xxxxxx",
            "xxxxxx",
            "xxxxxx",
            "xxxxxx",
            "xxxxxx",
            " xxxx ",
        ),
    ]
)


medium_set = symmetrize(
    [
        (
            "xxxx",
            "xxxx",
            "xxxx",
            "xxxx",
            " xx ",
        ),
        (
            "xxxx",
            "xxxx",
            "xxxx",
            "xxxx",
            "xxxx",
            " xx ",
        ),
        (
            " xxx ",
            "xxxxx",
            "xxxxx",
            " xxx ",
        ),
        (
            " xxx ",
            "xxxxx",
            "xxxxx",
            "xxxxx",
            " xxx ",
        ),
        (
            " xxx ",
            "xxxxx",
            "xxxxx",
            "xxxxx",
            "xxxxx",
            " xxx ",
        ),
        (
            "xxxxx",
            "xxxxx",
            "xxxxx",
            "xxxxx",
            " xxx ",
        ),
        (
            "xxxxx",
            "xxxxx",
            "xxxxx",
            "xxxxx",
            "xxxxx",
            " xxx ",
        ),
    ]
)

small_set = symmetrize(
    [
        (
            "xxx",
            "xxx",
            "xxx",
        ),
        (
            " xx ",
            "xxxx",
            "xxxx",
            " xx ",
        ),
        (
            " xxx",
            "xxxx",
            "xxxx",
            " xx ",
        ),
    ]
)


tiny_set = symmetrize(
    [
        (
            " xx",
            "xxx",
            "xx ",
        ),
    ]
)

one_grid_set = [
    ("x",),
]

tile_map = {"x": grf.OldIndustryTileID(0x10)}

the_industry = AIndustry(
    name="Forest",
    substitute_type=0x03,
    layouts=SplitDefinition(
        9,
        {
            0: transcribe(huge_set, tile_map),
            1: transcribe(large_set, tile_map),
            2: transcribe(medium_set, tile_map),
            3: transcribe(small_set, tile_map),
            4: transcribe(tiny_set, tile_map),
            5: transcribe(one_grid_set, tile_map),
            6: transcribe(one_grid_set, tile_map),
        },
    ),
    mapgen_probability=10,
    ingame_probability=4,
)
