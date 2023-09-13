from industry.lib.economy import Economy
from industry.industries import (
    bank,
    coal_mine,
    factory,
    farm,
    forest,
    iron_ore_mine,
    oil_refinery,
    oil_rig,
    oil_wells,
    power_station,
    sawmill,
    steel_mill,
)


the_economy = Economy(
    name="Vanilla Temperate",
    graph={
        bank: ((), ()),
        coal_mine: ((), ()),
        factory: ((), ()),
        farm: ((), ()),
        forest: ((), ()),
        iron_ore_mine: ((), ()),
        oil_refinery: ((), ()),
        oil_rig: ((), ()),
        oil_wells: ((), ()),
        power_station: ((), ()),
        sawmill: ((), ()),
        steel_mill: ((), ()),
    },
)
