from industry.lib.economy import Economy
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
)


the_economy = Economy(
    name="Vanilla Sub-Arctic",
    graph={
        bank: (gold, ()),
        coal_mine: ((), coal),
        food_processing_plant: (
            (
                livestock,
                wheat,
            ),
            food,
        ),
        farm: ((), (livestock, wheat)),
        forest: ((), wood),
        paper_mill: (wood, paper),
        oil_refinery: (oil, goods),
        printing_works: (paper, goods),
        oil_wells: ((), oil),
        power_station: (coal, ()),
        gold_mine: ((), gold),
    },
    town_cargos=(passengers, mail, food, goods),
)
