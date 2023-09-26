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


the_economy = Economy(
    name="Vanilla Sub-Arctic",
    graph={
        coal_mine: PrimaryIndustry(coal),
        farm: PrimaryIndustry((livestock, wheat)),
        forest: PrimaryIndustry(wood),
        oil_wells: PrimaryIndustry(oil),
        gold_mine: PrimaryIndustry((), gold),
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
