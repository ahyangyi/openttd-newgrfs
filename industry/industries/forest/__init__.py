import grf
from industry.lib.industry import AIndustry, SplitDefinition, transcribe
from .enormous import enormous_set
from .huge import huge_set
from .large import large_set
from .medium import medium_set
from .small import small_set
from .tiny import tiny_set


one_grid_set = [
    ("x",),
]

tile_map = {"x": grf.OldIndustryTileID(0x10)}

the_industry = AIndustry(
    translation_name="FOREST",
    override_type=0x03,
    layouts=SplitDefinition(
        ("INDUSTRY_SIZE",),
        {
            ("ENORMOUS",): transcribe(enormous_set, tile_map),
            ("HUGE",): transcribe(huge_set, tile_map),
            ("LARGE",): transcribe(large_set, tile_map),
            ("MEDIUM",): transcribe(medium_set, tile_map),
            ("SMALL",): transcribe(small_set, tile_map),
            ("TINY",): transcribe(tiny_set, tile_map),
            ("ONE_TILE",): transcribe(one_grid_set, tile_map),
            ("ONE_TILE_FLAT",): transcribe(one_grid_set, tile_map),
        },
    ),
    mapgen_probability=10,
    ingame_probability=4,
)
