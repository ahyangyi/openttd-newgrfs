from industry.lib.economy import Economy, PrimaryIndustry, SecondaryIndustry, TertiaryIndustry, Town
from industry.cargos import (
    copper_ore,
    food,
    goods,
    diamonds,
    mail,
    oil,
    passengers,
    maize,
    wood,
    fruit,
    rubber,
    farm_supplies,
    engineering_supplies,
)
from industry.industries import (
    bank,
    copper_ore_mine,
    food_processing_plant,
    farm,
    lumber_mill,
    fruit_plantation,
    rubber_plantation,
    oil_refinery,
    factory,
    oil_wells,
    diamond_mine,
    towns,
)


class TheEconomy:
    def __init__(self):
        self.name = "Vanilla Sub-Tropical"

    def get_economy(self, parameters):
        ret = Economy(
            {
                copper_ore_mine: PrimaryIndustry(copper_ore),
                oil_wells: PrimaryIndustry(oil),
                diamond_mine: PrimaryIndustry(diamonds),
                farm: PrimaryIndustry(maize),
                lumber_mill: PrimaryIndustry(wood),
                fruit_plantation: PrimaryIndustry(fruit),
                rubber_plantation: PrimaryIndustry(rubber),
                food_processing_plant: SecondaryIndustry((fruit, maize), food),
                oil_refinery: SecondaryIndustry(oil, goods),
                factory: SecondaryIndustry((rubber, copper_ore, wood), goods),
                bank: TertiaryIndustry(diamonds),
                towns: Town(passengers, mail, food, goods),
            },
            parameters,
        )
        if parameters["BOOSTER"] == "UNIVERSAL":
            ret.graph[diamond_mine].booster = engineering_supplies
            ret.graph[oil_wells].booster = engineering_supplies
            ret.graph[copper_ore_mine].booster = engineering_supplies
            ret.graph[farm].booster = engineering_supplies
            ret.graph[lumber_mill].booster = engineering_supplies

            ret.graph[factory].produces += (engineering_supplies,)
        elif parameters["BOOSTER"] == "GENERIC":
            ret.graph[diamond_mine].booster = engineering_supplies
            ret.graph[oil_wells].booster = engineering_supplies
            ret.graph[copper_ore_mine].booster = engineering_supplies
            ret.graph[farm].booster = farm_supplies
            ret.graph[lumber_mill].booster = farm_supplies

            ret.graph[factory].produces += (engineering_supplies,)
            ret.graph[oil_refinery].produces += (farm_supplies,)
        return ret
