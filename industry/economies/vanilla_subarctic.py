from industry.lib.economy import Economy, PrimaryIndustry, SecondaryIndustry, TertiaryIndustry, Town
from industry.cargos import (
    coal,
    food,
    goods,
    gold,
    livestock,
    mail,
    oil,
    paper,
    passengers,
    wheat,
    wood,
    farm_supplies,
    engineering_supplies,
)
from industry.industries import (
    bank,
    coal_mine,
    food_processing_plant,
    farm,
    forest,
    paper_mill,
    oil_refinery,
    printing_works,
    oil_wells,
    power_station,
    gold_mine,
    towns,
    port,
    trading_centre,
)


class TheEconomy:
    def __init__(self):
        self.name = "Vanilla Sub-Arctic"

    def get_economy(self, parameters):
        ret = Economy(
            {
                coal_mine: PrimaryIndustry(coal),
                farm: PrimaryIndustry((livestock, wheat)),
                forest: PrimaryIndustry(wood),
                oil_wells: PrimaryIndustry(oil),
                gold_mine: PrimaryIndustry(gold),
                food_processing_plant: SecondaryIndustry(
                    (
                        livestock,
                        wheat,
                    ),
                    food,
                ),
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
            ret.graph[port] = SecondaryIndustry(wood, paper)
        elif parameters["POLICY"] in ("FREE_TRADE", "EXPORT"):
            ret.graph[port] = SecondaryIndustry(wood, paper)
            del ret.graph[paper_mill]

        if parameters["BOOSTER"] == "UNIVERSAL":
            ret.graph[coal_mine].booster = engineering_supplies
            ret.graph[oil_wells].booster = engineering_supplies
            ret.graph[gold_mine].booster = engineering_supplies
            ret.graph[farm].booster = engineering_supplies
            ret.graph[forest].booster = engineering_supplies

            ret.graph[printing_works].produces += (engineering_supplies,)
        elif parameters["BOOSTER"] == "GENERIC":
            ret.graph[coal_mine].booster = engineering_supplies
            ret.graph[oil_wells].booster = engineering_supplies
            ret.graph[gold_mine].booster = engineering_supplies
            ret.graph[farm].booster = farm_supplies
            ret.graph[forest].booster = farm_supplies

            ret.graph[printing_works].produces += (engineering_supplies,)
            ret.graph[oil_refinery].produces += (farm_supplies,)

        if port in ret.graph:
            if parameters["LAND_PORTS"] == "LAND_ONLY":
                ret.graph[trading_centre] = ret.graph[port]
                del ret.graph[port]
            elif parameters["LAND_PORTS"] == "BOTH":
                ret.graph[trading_centre] = ret.graph[port]

        return ret
