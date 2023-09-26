from industry.lib.economy import Economy, PrimaryIndustry, SecondaryIndustry, TertiaryIndustry, Town
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
    towns,
)


the_economy = Economy(
    name="Vanilla Temperate",
    graph={
        coal_mine: PrimaryIndustry(coal),
        bank: PrimaryIndustry(valuables, valuables),
        farm: PrimaryIndustry((grain, livestock)),
        forest: PrimaryIndustry(wood),
        iron_ore_mine: PrimaryIndustry(iron_ore),
        oil_rig: PrimaryIndustry(oil),
        oil_wells: PrimaryIndustry(oil),
        factory: SecondaryIndustry((grain, livestock, steel), goods),
        oil_refinery: SecondaryIndustry(oil, goods),
        sawmill: SecondaryIndustry(wood, goods),
        steel_mill: SecondaryIndustry(iron_ore, steel),
        power_station: TertiaryIndustry(coal),
        towns: Town(passengers, mail, None, goods),
    },
)
