import grf
from industry.lib.industry import AIndustry, transcribe, symmetrize


medium_set = [
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


the_industry = AIndustry(
    name="Forest",
    substitute_type=0x03,
    layouts=transcribe(symmetrize(medium_set), {"x": grf.OldIndustryTileID(0x10)}),
)
