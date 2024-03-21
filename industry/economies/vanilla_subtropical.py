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
    water,
    wood,
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
    port,
    rubber_plantation,
    towns,
    water_supply,
    water_tower,
)


class TheEconomy(MetaEconomy):
    def __init__(self):
        super().__init__("VANILLA_SUBTROPICAL")

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
        if parameters["POLICY"] == "SELF_SUFFICIENT":
            ret.graph[port] = FreePort(diamonds, oil)
        elif parameters["POLICY"] in ("FREE_TRADE", "EXPORT"):
            ret.graph[port] = FreePort(diamonds, oil)

        if parameters["PRIMARY_INDUSTRY_GROWTH"] == "UNIVERSAL_SUPPLIES":
            ret.graph[diamond_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies
            ret.graph[copper_ore_mine].boosters = engineering_supplies
            ret.graph[farm].boosters = engineering_supplies
            ret.graph[lumber_mill].boosters = engineering_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies,)
            else:
                ret.graph[factory].produces += (engineering_supplies,)
        elif parameters["PRIMARY_INDUSTRY_GROWTH"] == "GENERIC_SUPPLIES":
            ret.graph[diamond_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies
            ret.graph[copper_ore_mine].boosters = engineering_supplies
            ret.graph[farm].boosters = farm_supplies
            ret.graph[lumber_mill].boosters = farm_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies, farm_supplies)
            else:
                ret.graph[factory].produces += (engineering_supplies,)
                ret.graph[oil_refinery].produces += (farm_supplies,)

        self.default_worker_support(
            ret,
            (goods, diamonds),
            (diamond_mine,),
            (diamond_mine, oil_wells, copper_ore_mine, farm, lumber_mill),
            (food_processing_plant, oil_refinery, factory),
        )

        if parameters["TOWN_GOODS"] in ("ORGANIC", "FOOD_AND_WATER"):
            ret.graph[water_supply] = PrimaryIndustry(water)
            ret.graph[water_tower] = TertiaryIndustry(water)

        return ret
