from industry.lib.economy import Economy, PrimaryIndustry, SecondaryIndustry, TertiaryIndustry, Town
from industry.cargos import (
    ammonia,
    china_clay,
    engineering_supplies,
    explosives,
    farm_supplies,
    fertiliser,
    food,
    goods,
    mail,
    paper,
    passengers,
    peat,
    phosphate,
    potash,
    pyrite_ore,
    pyrite_ore,
    sulphur,
    timber,
    water,
    wood,
    workers,
    zinc,
)
from industry.industries import (
    ammonia_plant,
    chemical_plant,
    clay_pit,
    forest,
    general_store,
    herding_coop,
    paper_mill,
    peatlands,
    phosphate_mine,
    port,
    potash_mine,
    power_station,
    pyrite_mine,
    pyrite_mine,
    pyrite_smelter,
    sawmill,
    towns,
    trading_centre,
    water_supply,
    water_tower,
    worker_yard,
)


class TheEconomy:
    def __init__(self):
        self.name = "FIRS Arctic"

    def get_economy(self, parameters):
        ret = Economy(
            {
                ammonia_plant: PrimaryIndustry(ammonia),
                clay_pit: PrimaryIndustry(china_clay),
                forest: PrimaryIndustry(wood),
                pyrite_mine: PrimaryIndustry(pyrite_ore),
                phosphate_mine: PrimaryIndustry(phosphate),
                potash_mine: PrimaryIndustry(potash),
                peatlands: PrimaryIndustry(peat),
                herding_coop: PrimaryIndustry(food),
                pyrite_smelter: SecondaryIndustry(pyrite_ore, (sulphur, zinc)),
                sawmill: SecondaryIndustry(wood, timber),
                chemical_plant: SecondaryIndustry(
                    (phosphate, sulphur, ammonia, potash),
                    (explosives, fertiliser),
                ),
                paper_mill: SecondaryIndustry((wood, sulphur, china_clay), paper),
                power_station: TertiaryIndustry(peat),
                general_store: TertiaryIndustry((explosives, fertiliser, zinc, timber)),
                towns: Town(passengers, mail, food, paper),
            },
            parameters,
        )
        if parameters["POLICY"] == "SELF_SUFFICIENT":
            ret.graph[port] = SecondaryIndustry(timber, china_clay)
        elif parameters["POLICY"] in ("FREE_TRADE", "EXPORT"):
            ret.graph[port] = SecondaryIndustry(timber, china_clay)
            del ret.graph[clay_pit]

        if parameters["BOOSTER"] == "UNIVERSAL":
            ret.graph[ammonia_plant].booster = engineering_supplies
            ret.graph[peatlands].booster = engineering_supplies
            ret.graph[pyrite_mine].booster = engineering_supplies
            ret.graph[herding_coop].booster = engineering_supplies
            ret.graph[forest].booster = engineering_supplies

            ret.graph[paper_mill].produces += (engineering_supplies,)
        elif parameters["BOOSTER"] == "GENERIC":
            ret.graph[ammonia_plant].booster = engineering_supplies
            ret.graph[peatlands].booster = engineering_supplies
            ret.graph[pyrite_mine].booster = engineering_supplies
            ret.graph[herding_coop].booster = farm_supplies
            ret.graph[forest].booster = farm_supplies

            ret.graph[paper_mill].produces += (engineering_supplies,)
            ret.graph[chemical_plant].produces += (farm_supplies,)
        elif parameters["BOOSTER"] == "GENERIC_PASSENGERS":
            ret.graph[ammonia_plant].booster = engineering_supplies
            ret.graph[peatlands].booster = engineering_supplies
            ret.graph[pyrite_mine].booster = engineering_supplies
            ret.graph[herding_coop].booster = farm_supplies
            ret.graph[forest].booster = farm_supplies

            ret.graph[paper_mill].produces += (engineering_supplies,)
            ret.graph[chemical_plant].produces += (farm_supplies,)

        if parameters["WORKER"].startswith("YETI"):
            ret.graph[worker_yard] = PrimaryIndustry(workers)

            # FIXME
            ret.graph[peatlands].booster = workers

        if port in ret.graph:
            if parameters["LAND_PORTS"] == "LAND_ONLY":
                ret.graph[trading_centre] = ret.graph[port]
                del ret.graph[port]
            elif parameters["LAND_PORTS"] == "BOTH":
                ret.graph[trading_centre] = ret.graph[port]

        if parameters["TOWN_GOODS"] == "SUBTROPICAL":
            ret.graph[water_supply] = PrimaryIndustry(water)
            ret.graph[water_tower] = TertiaryIndustry(water)

        return ret
