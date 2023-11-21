from industry.lib.economy import (
    MetaEconomy,
    Economy,
    PrimaryIndustry,
    WorkerYard,
    FreePort,
    SecondaryIndustry,
    TertiaryIndustry,
    Town,
)
from industry.cargos import (
    alcohol,
    beans,
    chemicals,
    coffee,
    copper,
    copper_ore,
    engineering_supplies,
    farm_supplies,
    fish,
    food,
    fruit,
    goods,
    grain,
    livestock,
    mail,
    nitrates,
    oil,
    passengers,
    tired_workers,
    water,
    wool,
    workers,
    zinc,
)
from industry.industries import (
    arable_farm,
    chemical_plant,
    coffee_estate,
    copper_ore_mine,
    copper_smelter,
    fishing_grounds,
    fishing_harbor,
    flour_mill,
    food_processing_plant,
    general_store,
    nitrate_mine,
    oil_wells,
    port,
    ranch,
    stockyard,
    towns,
    trading_centre,
    vineyard,
    water_supply,
    water_tower,
    worker_yard,
)


class TheEconomy(MetaEconomy):
    def __init__(self):
        super().__init__("BASIC_TROPICAL")

    def get_economy(self, parameters):
        ret = Economy(
            {
                copper_ore_mine: PrimaryIndustry(copper_ore),
                nitrate_mine: PrimaryIndustry(nitrates),
                oil_wells: PrimaryIndustry(oil),
                arable_farm: PrimaryIndustry((grain, beans)),
                fishing_grounds: PrimaryIndustry(fish),
                coffee_estate: PrimaryIndustry((fruit, coffee)),
                ranch: PrimaryIndustry((livestock, wool)),
                vineyard: PrimaryIndustry((fruit, alcohol)),
                copper_smelter: SecondaryIndustry((copper_ore, chemicals), copper),
                food_processing_plant: SecondaryIndustry((beans, fruit), food),
                stockyard: SecondaryIndustry(livestock, food),
                flour_mill: SecondaryIndustry(grain, food),
                chemical_plant: SecondaryIndustry((nitrates, oil), chemicals),
                fishing_harbor: SecondaryIndustry(fish, food),
                general_store: TertiaryIndustry((alcohol, food, goods, wool, copper, coffee)),
                towns: Town(passengers, mail, food, goods),
            },
            parameters,
        )
        if parameters["POLICY"] == "SELF_SUFFICIENT":
            ret.graph[port] = FreePort((alcohol, coffee, wool, copper, food, chemicals), goods)
            del ret.graph[general_store]  # FIXME
        elif parameters["POLICY"] in ("FREE_TRADE", "EXPORT"):
            ret.graph[port] = FreePort((alcohol, coffee, wool, copper, food, chemicals), goods)
            del ret.graph[general_store]  # FIXME
        else:
            ret.graph[towns].goods = alcohol
            ret.graph[general_store].consumes = (alcohol, food, wool, copper, coffee)

        if parameters["PRIMARY_INDUSTRY_GROWTH"] == "UNIVERSAL_SUPPLIES":
            if nitrate_mine in ret.graph:
                ret.graph[nitrate_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies
            ret.graph[copper_ore_mine].boosters = engineering_supplies

            ret.graph[vineyard].boosters = engineering_supplies
            ret.graph[arable_farm].boosters = engineering_supplies
            ret.graph[coffee_estate].boosters = engineering_supplies
            ret.graph[ranch].boosters = engineering_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies,)
            else:
                ret.graph[chemical_plant].produces += (engineering_supplies,)

        elif parameters["PRIMARY_INDUSTRY_GROWTH"] == "GENERIC_SUPPLIES":
            if nitrate_mine in ret.graph:
                ret.graph[nitrate_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies
            ret.graph[copper_ore_mine].boosters = engineering_supplies

            ret.graph[vineyard].boosters = farm_supplies
            ret.graph[arable_farm].boosters = farm_supplies
            ret.graph[coffee_estate].boosters = farm_supplies
            ret.graph[ranch].boosters = farm_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies, farm_supplies)
            else:
                ret.graph[copper_smelter].produces += (engineering_supplies,)
                ret.graph[chemical_plant].produces += (farm_supplies,)

        if parameters["WORKFORCE"].startswith("YETI"):
            if parameters["WORKFORCE"] == "YETI":
                ret.graph[worker_yard] = WorkerYard(workers, boosters=(food, wool))
            elif parameters["WORKFORCE"] == "YETI_PASSENGERS":
                ret.graph[worker_yard] = WorkerYard(workers, boosters=(food, wool, passengers))
            elif parameters["WORKFORCE"] == "YETI_MAIL":
                ret.graph[worker_yard] = WorkerYard(workers, boosters=(food, wool, mail))
            elif parameters["WORKFORCE"] == "YETI_TIRED":
                ret.graph[worker_yard] = WorkerYard(workers, boosters=(food, wool, tired_workers))

            # FIXME: remove PRESET; support SECONDARY
            if parameters["WORKER_PARTICIPATION"] in ("PRESET", "NONE"):
                ret.graph[fishing_grounds].boosters = workers
                if parameters["WORKFORCE"] == "YETI_TIRED":
                    ret.graph[fishing_grounds].produces += (tired_workers,)
            if parameters["WORKER_PARTICIPATION"] in ("PRIMARY_INDUSTRY", "SECONDARY_INDUSTRY", "BOTH"):
                for i in [
                    nitrate_mine,
                    oil_wells,
                    copper_ore_mine,
                    vineyard,
                    arable_farm,
                    ranch,
                ]:
                    if i in ret.graph:
                        ret.graph[i] = ret.graph[i].to_secondary(workers)
                        if parameters["WORKFORCE"] == "YETI_TIRED":
                            ret.graph[i].produces += (tired_workers,)

        if port in ret.graph:
            if parameters["SEA_INDUSTRY"] == "LAND_ONLY":
                ret.graph[trading_centre] = ret.graph[port]
                del ret.graph[port]
            elif parameters["SEA_INDUSTRY"] == "BOTH":
                ret.graph[trading_centre] = ret.graph[port]

        if parameters["TOWN_GOODS"] == "FOOD_AND_WATER":
            ret.graph[water_supply] = PrimaryIndustry(water)
            ret.graph[water_tower] = TertiaryIndustry(water)

        return ret
