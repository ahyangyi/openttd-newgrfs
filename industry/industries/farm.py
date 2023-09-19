import grf
from industry.lib.industry import AIndustry


the_industry = AIndustry(
    id=0x28,
    name="Farm",
    substitute_type=0x09,
    layouts=[[{"xofs": i, "yofs": j, "gfx": grf.NewIndustryTileID(0x23)} for i in range(4) for j in range(4)]],
)
