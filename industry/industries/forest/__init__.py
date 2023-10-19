import grf
from industry.lib.industry import AIndustry, SplitDefinition, transcribe, symmetrize
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
    name="Forest",
    override_type=0x03,
    layouts=SplitDefinition(
        9,
        {
            0: transcribe(enormous_set, tile_map),
            1: transcribe(huge_set, tile_map),
            2: transcribe(large_set, tile_map),
            3: transcribe(medium_set, tile_map),
            4: transcribe(small_set, tile_map),
            5: transcribe(tiny_set, tile_map),
            6: transcribe(one_grid_set, tile_map),
            7: transcribe(one_grid_set, tile_map),
        },
    ),
    mapgen_probability=10,
    ingame_probability=4,
)
