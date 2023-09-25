from industry.lib.economy import Economy
from industry.cargos import (
    valuables,
    coal,
    grain,
    livestock,
    steel,
    goods,
    wood,
    iron_ore,
    oil,
    passengers,
    mail,
)
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
        bank: (valuables, valuables),
        coal_mine: ((), coal),
        factory: ((grain, livestock, steel), goods),
        farm: ((), (grain, livestock)),
        forest: ((), wood),
        iron_ore_mine: ((), iron_ore),
        oil_refinery: (oil, goods),
        oil_rig: ((), oil),
        oil_wells: ((), oil),
        power_station: (coal, ()),
        sawmill: (wood, goods),
        steel_mill: (iron_ore, steel),
    },
    town_cargos=(passengers, mail, None, goods),
)
