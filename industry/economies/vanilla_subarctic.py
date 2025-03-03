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
    coal,
    engineering_supplies,
    farm_supplies,
    food,
    gold,
    goods,
    livestock,
    mail,
    oil,
    paper,
    passengers,
    water,
    wheat,
    wood,
)
from industry.industries import (
    bank,
    coal_mine,
    farm,
    food_processing_plant,
    forest,
    gold_mine,
    oil_refinery,
    oil_wells,
    paper_mill,
    port,
    power_station,
    printing_works,
    towns,
    trading_centre,
    water_supply,
    water_tower,
)


class TheEconomy(MetaEconomy):
    def __init__(self):
        super().__init__("VANILLA_SUBARCTIC")

    def get_economy(self, parameters):
        ret = Economy(
            {
                coal_mine: PrimaryIndustry(coal),
                farm: PrimaryIndustry((livestock, wheat)),
                forest: PrimaryIndustry(wood),
                oil_wells: PrimaryIndustry(oil),
                gold_mine: PrimaryIndustry(gold),
                food_processing_plant: SecondaryIndustry((livestock, wheat), food),
                paper_mill: SecondaryIndustry(wood, paper),
                oil_refinery: SecondaryIndustry(oil, goods),
                printing_works: SecondaryIndustry(paper, goods),
                power_station: TertiaryIndustry(coal),
                bank: TertiaryIndustry(gold),
                towns: Town(passengers, mail, food, goods),
            },
            parameters,
        )
        if parameters["POLICY"] == "SELF_SUFFICIENT":
            ret.graph[port] = FreePort(wood, paper)
        elif parameters["POLICY"] in ("FREE_TRADE", "EXPORT"):
            ret.graph[port] = FreePort(wood, paper)
            del ret.graph[paper_mill]

        if parameters["PRIMARY_INDUSTRY_GROWTH"] == "UNIVERSAL_SUPPLIES":
            ret.graph[coal_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies
            ret.graph[gold_mine].boosters = engineering_supplies
            ret.graph[farm].boosters = engineering_supplies
            ret.graph[forest].boosters = engineering_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies,)
            else:
                ret.graph[printing_works].produces += (engineering_supplies,)
        elif parameters["PRIMARY_INDUSTRY_GROWTH"] == "GENERIC_SUPPLIES":
            ret.graph[coal_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = engineering_supplies
            ret.graph[gold_mine].boosters = engineering_supplies
            ret.graph[farm].boosters = farm_supplies
            ret.graph[forest].boosters = farm_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies, farm_supplies)
            else:
                ret.graph[printing_works].produces += (engineering_supplies,)
                ret.graph[oil_refinery].produces += (farm_supplies,)
        elif parameters["PRIMARY_INDUSTRY_GROWTH"] == "GENERIC_SUPPLIES_PASSENGERS":
            ret.graph[coal_mine].boosters = engineering_supplies
            ret.graph[oil_wells].boosters = passengers
            ret.graph[gold_mine].boosters = engineering_supplies
            ret.graph[farm].boosters = farm_supplies
            ret.graph[forest].boosters = farm_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies, farm_supplies)
            else:
                ret.graph[printing_works].produces += (engineering_supplies,)
                ret.graph[oil_refinery].produces += (farm_supplies,)

        self.default_worker_support(
            ret,
            (goods, gold),
            (coal_mine,),
            (coal_mine, oil_wells, gold_mine, farm, forest),
            (food_processing_plant, paper_mill, oil_refinery, printing_works),
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
