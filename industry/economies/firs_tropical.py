from industry.lib.economy import (
    MetaEconomy,
    Economy,
    PrimaryIndustry,
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
    water,
    wool,
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
            ret.graph[copper_ore_mine].boosters = engineering_supplies
            ret.graph[nitrate_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies

            ret.graph[arable_farm].boosters = engineering_supplies
            ret.graph[coffee_estate].boosters = engineering_supplies
            ret.graph[ranch].boosters = engineering_supplies
            ret.graph[vineyard].boosters = engineering_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies,)
            else:
                ret.graph[copper_smelter].produces += (engineering_supplies,)

        elif parameters["PRIMARY_INDUSTRY_GROWTH"] == "GENERIC_SUPPLIES":
            ret.graph[copper_ore_mine].boosters = engineering_supplies
            ret.graph[nitrate_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies

            ret.graph[arable_farm].boosters = farm_supplies
            ret.graph[coffee_estate].boosters = farm_supplies
            ret.graph[ranch].boosters = farm_supplies
            ret.graph[vineyard].boosters = farm_supplies

            ret.graph[nitrate_mine].produces += (farm_supplies,)
            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies, farm_supplies)
            else:
                ret.graph[copper_smelter].produces += (engineering_supplies,)

        self.default_worker_support(
            ret,
            (food, wool),
            (fishing_grounds,),
            (copper_ore_mine, nitrate_mine, oil_wells, arable_farm, coffee_estate, fishing_grounds, ranch, vineyard),
            (chemical_plant, copper_smelter, fishing_harbor, flour_mill, stockyard, food_processing_plant),
        )

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
