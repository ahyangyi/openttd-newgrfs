import grf
from industry.lib.industry import AIndustry, SplitDefinition, transcribe, symmetrize
from .enormous import enormous_set
from .huge import huge_set
from .large import large_set
from .medium import medium_set


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
    translation_name="OIL_WELLS",
    override_type=0x0B,
    layouts=SplitDefinition(
        ("INDUSTRY_SIZE",),
        {
            ("ENORMOUS",): transcribe(enormous_set, tile_map),
            ("HUGE",): transcribe(huge_set, tile_map),
            ("LARGE",): transcribe(large_set, tile_map),
            ("MEDIUM",): transcribe(medium_set, tile_map),
            ("SMALL",): transcribe(small_set, tile_map),
            ("TINY",): transcribe(tiny_set, tile_map),
            ("ONE_TILE",): transcribe(one_tile_set, tile_map),
            ("ONE_TILE_FLAT",): [[{"xofs": 0, "yofs": 0, "gfx": grf.NewIndustryTileID(0x23)}]],
        },
    ),
    mapgen_probability=6,
    ingame_probability=6,
)
