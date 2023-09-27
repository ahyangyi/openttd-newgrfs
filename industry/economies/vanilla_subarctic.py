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
)


class SubArcticEconomy(Economy):
    def __init__(self):
        super().__init__(
            name="Vanilla Sub-Arctic",
            graph={
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
        )

    def set_economy_policy(self, policy):
        super().set_economy_policy(policy)

    def set_economy_booster(self, booster):
        super().set_economy_booster(booster)

        if booster == "generic":
            self.graph[coal_mine].booster = engineering_supplies
            self.graph[oil_wells].booster = engineering_supplies
            self.graph[gold_mine].booster = engineering_supplies
            self.graph[farm].booster = farm_supplies
            self.graph[forest].booster = farm_supplies


the_economy = SubArcticEconomy()
