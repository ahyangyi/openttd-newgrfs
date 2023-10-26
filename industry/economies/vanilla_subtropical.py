from industry.lib.economy import Economy, PrimaryIndustry, WorkerYard, SecondaryIndustry, TertiaryIndustry, Town
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
    water,
    farm_supplies,
    engineering_supplies,
    workers,
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
    water_supply,
    water_tower,
    worker_yard,
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
            ret.graph[diamond_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies
            ret.graph[copper_ore_mine].boosters = engineering_supplies
            ret.graph[farm].boosters = engineering_supplies
            ret.graph[lumber_mill].boosters = engineering_supplies

            ret.graph[factory].produces += (engineering_supplies,)
        elif parameters["BOOSTER"] == "GENERIC":
            ret.graph[diamond_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies
            ret.graph[copper_ore_mine].boosters = engineering_supplies
            ret.graph[farm].boosters = farm_supplies
            ret.graph[lumber_mill].boosters = farm_supplies

            ret.graph[factory].produces += (engineering_supplies,)
            ret.graph[oil_refinery].produces += (farm_supplies,)

        if parameters["WORKFORCE"].startswith("YETI"):
            ret.graph[worker_yard] = WorkerYard(workers, boosters=(goods, diamonds))
            # FIXME
            ret.graph[diamond_mine].boosters = workers

        if parameters["TOWN_GOODS"] in ("ORGANIC", "SUBTROPICAL"):
            ret.graph[water_supply] = PrimaryIndustry(water)
            ret.graph[water_tower] = TertiaryIndustry(water)

        return ret
