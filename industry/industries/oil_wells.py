import grf
from industry.lib.industry import AIndustry, transcribe, symmetrize


medium_set = [
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

the_industry = AIndustry(
    name="Oil Wells",
    substitute_type=0x0B,
    layouts=transcribe(symmetrize(medium_set), {"x": grf.OldIndustryTileID(0x1D)}),
)
