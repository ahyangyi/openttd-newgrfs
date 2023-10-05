import grf
from industry.lib.industry import AIndustry, transcribe, symmetrize

medium_set = [
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
    #    layouts=[[{"xofs": i, "yofs": j, "gfx": grf.NewIndustryTileID(0x23)} for i in range(4) for j in range(4)]],
    layouts=transcribe(symmetrize(medium_set), tile_map),
)
