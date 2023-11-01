from industry.lib.economy import Economy, PrimaryIndustry, WorkerYard, SecondaryIndustry, TertiaryIndustry, Town
from industry.cargos import (
    copper_ore,
    diamonds,
    engineering_supplies,
    farm_supplies,
    food,
    fruit,
    goods,
    mail,
    maize,
    oil,
    passengers,
    rubber,
    tired_workers,
    water,
    wood,
    workers,
)
from industry.industries import (
    bank,
    copper_ore_mine,
    diamond_mine,
    factory,
    farm,
    food_processing_plant,
    fruit_plantation,
    lumber_mill,
    oil_refinery,
    oil_wells,
    rubber_plantation,
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
            if parameters["WORKFORCE"] == "YETI":
                ret.graph[worker_yard] = WorkerYard(workers, boosters=(goods, diamonds))
            elif parameters["WORKFORCE"] == "YETI_PASSENGERS":
                ret.graph[worker_yard] = WorkerYard(workers, boosters=(goods, diamonds, passengers))
            elif parameters["WORKFORCE"] == "YETI_MAIL":
                ret.graph[worker_yard] = WorkerYard(workers, boosters=(goods, diamonds, mail))
            elif parameters["WORKFORCE"] == "YETI_TIRED":
                ret.graph[worker_yard] = WorkerYard(workers, boosters=(goods, diamonds, tired_workers))
                ret.graph[diamond_mine].produces += (tired_workers,)
            # FIXME
            ret.graph[diamond_mine].boosters = workers

        if parameters["TOWN_GOODS"] in ("ORGANIC", "SUBTROPICAL"):
            ret.graph[water_supply] = PrimaryIndustry(water)
            ret.graph[water_tower] = TertiaryIndustry(water)

        return ret
