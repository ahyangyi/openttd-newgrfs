import grf
from industry.lib.industry import AIndustry


the_industry = AIndustry(
    name="Forest",
    substitute_type=0x03,
    layouts=[[{"xofs": i, "yofs": j, "gfx": grf.OldIndustryTileID(0x10)} for i in range(4) for j in range(4)]],
)
