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
    farm_supplies,
    engineering_supplies,
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


class TheEconomy:
    def __init__(self):
        self.name = "Vanilla Temperate"

    def get_economy(self, parameters):
        ret = Economy(
            {
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
            parameters,
        )
        if parameters["BOOSTER"] == "UNIVERSAL":
            ret.graph[coal_mine].booster = engineering_supplies
            ret.graph[oil_wells].booster = engineering_supplies
            ret.graph[oil_rig].booster = engineering_supplies
            ret.graph[iron_ore_mine].booster = engineering_supplies
            ret.graph[farm].booster = engineering_supplies
            ret.graph[forest].booster = engineering_supplies

            ret.graph[factory].produces += (engineering_supplies,)
        elif parameters["BOOSTER"] == "GENERIC":
            ret.graph[coal_mine].booster = engineering_supplies
            ret.graph[oil_wells].booster = engineering_supplies
            ret.graph[oil_rig].booster = engineering_supplies
            ret.graph[iron_ore_mine].booster = engineering_supplies
            ret.graph[farm].booster = farm_supplies
            ret.graph[forest].booster = farm_supplies

            ret.graph[factory].produces += (engineering_supplies,)
            ret.graph[oil_refinery].produces += (farm_supplies,)
        return ret
