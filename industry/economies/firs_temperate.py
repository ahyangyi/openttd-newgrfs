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
    chemicals,
    china_clay,
    coal,
    engineering_supplies,
    farm_supplies,
    fish,
    food,
    fruit,
    goods,
    iron_ore,
    livestock,
    mail,
    milk,
    passengers,
    sand,
    scrap_metal,
    steel,
    tired_workers,
    water,
    workers,
)
from industry.industries import (
    chemical_plant,
    cider_mill,
    clay_pit,
    coal_mine,
    dairy,
    dairy_farm,
    dredging_site,
    fishing_grounds,
    fishing_harbor,
    general_store,
    glass_works,
    iron_ore_mine,
    metal_workshop,
    orchard_and_piggery,
    port,
    scrap_yard,
    steel_mill,
    stockyard,
    towns,
    trading_centre,
    water_supply,
    water_tower,
    worker_yard,
)


class TheEconomy(MetaEconomy):
    def __init__(self):
        super().__init__("BASIC_TEMPERATE")

    def get_economy(self, parameters):
        ret = Economy(
            {
                clay_pit: PrimaryIndustry(china_clay),
                coal_mine: PrimaryIndustry(coal),
                dredging_site: PrimaryIndustry(sand),
                iron_ore_mine: PrimaryIndustry(iron_ore),
                scrap_yard: PrimaryIndustry(scrap_metal),
                fishing_grounds: PrimaryIndustry(fish),
                dairy_farm: PrimaryIndustry((milk, livestock)),
                orchard_and_piggery: PrimaryIndustry((fruit, livestock)),
                chemical_plant: PrimaryIndustry(chemicals),
                steel_mill: SecondaryIndustry((coal, iron_ore, scrap_metal), steel),
                dairy: SecondaryIndustry(milk, food),
                glass_works: SecondaryIndustry((sand, chemicals), goods),
                metal_workshop: SecondaryIndustry((steel, chemicals), goods),
                fishing_harbor: SecondaryIndustry(fish, food),
                cider_mill: SecondaryIndustry(fruit, alcohol),
                stockyard: SecondaryIndustry(livestock, food),
                general_store: TertiaryIndustry((alcohol, food, goods, china_clay)),
                towns: Town(passengers, mail, food, goods),
            },
            parameters,
        )
        if parameters["POLICY"] == "SELF_SUFFICIENT":
            ret.graph[port] = FreePort((goods, food, china_clay), chemicals)
        elif parameters["POLICY"] in ("FREE_TRADE", "EXPORT"):
            ret.graph[port] = FreePort((goods, food, china_clay), chemicals)
            del ret.graph[chemical_plant]

        if parameters["PRIMARY_INDUSTRY_GROWTH"] == "UNIVERSAL_SUPPLIES":
            ret.graph[clay_pit].boosters = engineering_supplies
            ret.graph[coal_mine].boosters = engineering_supplies
            ret.graph[dredging_site].boosters = engineering_supplies
            ret.graph[iron_ore_mine].boosters = engineering_supplies
            ret.graph[dairy_farm].boosters = engineering_supplies
            ret.graph[orchard_and_piggery].boosters = engineering_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies,)
            else:
                ret.graph[metal_workshop].produces += (engineering_supplies,)
        elif parameters["PRIMARY_INDUSTRY_GROWTH"] == "GENERIC_SUPPLIES":
            ret.graph[clay_pit].boosters = engineering_supplies
            ret.graph[coal_mine].boosters = engineering_supplies
            ret.graph[dredging_site].boosters = engineering_supplies
            ret.graph[iron_ore_mine].boosters = engineering_supplies
            ret.graph[dairy_farm].boosters = farm_supplies
            ret.graph[orchard_and_piggery].boosters = farm_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies, farm_supplies)
            else:
                ret.graph[metal_workshop].produces += (engineering_supplies,)
                ret.graph[glass_works].produces += (farm_supplies,)
        elif parameters["PRIMARY_INDUSTRY_GROWTH"] == "GENERIC_SUPPLIES_PASSENGERS":
            ret.graph[clay_pit].boosters = engineering_supplies
            ret.graph[coal_mine].boosters = engineering_supplies
            ret.graph[dredging_site].boosters = engineering_supplies
            ret.graph[iron_ore_mine].boosters = engineering_supplies
            ret.graph[dairy_farm].boosters = farm_supplies
            ret.graph[orchard_and_piggery].boosters = farm_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies, farm_supplies)
            else:
                ret.graph[metal_workshop].produces += (engineering_supplies,)
                ret.graph[glass_works].produces += (farm_supplies,)

        self.default_worker_support(
            ret,
            (goods, alcohol),
            (fishing_grounds,),
            (chemical_plant, clay_pit, coal_mine, dredging_site, iron_ore_mine, dairy_farm, orchard_and_piggery),
            (metal_workshop, steel_mill, glass_works, cider_mill, stockyard, fishing_harbor, dairy),
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
